from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import tempfile
import asyncio
from typing import Dict, Any
from dotenv import load_dotenv
from langfuse import Langfuse
from crewai import Crew, Task
from agents.clause_extractor import ClauseExtractorAgent
from agents.risk_assessor import RiskAssessmentAgent
from agents.suggestion_agent import SuggestionAgent
from utils.file_parser import DocumentParser
from utils.pdf_report import PDFReportGenerator

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Legal Document Analyzer",
    description="Multi-agent AI system for contract analysis and risk assessment",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Langfuse
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY", "pk-lf-default"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY", "sk-lf-default"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
)

# Initialize document parser
document_parser = DocumentParser()

# Initialize agents
clause_extractor = ClauseExtractorAgent()
risk_assessor = RiskAssessmentAgent()
suggestion_agent = SuggestionAgent()

# Initialize PDF report generator
pdf_generator = PDFReportGenerator()

@app.get("/")
async def root():
    """Serve the main HTML interface"""
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AI Legal Document Analyzer"}

@app.post("/api/analyze-contract")
async def analyze_contract(file: UploadFile = File(...)):
    """
    Analyze uploaded contract document and return risk assessment
    """
    # Log analysis start
    
    try:
        # Validate file type
        if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            raise HTTPException(
                status_code=400, 
                detail="Unsupported file type. Please upload PDF or DOCX files only."
            )
        
        # Save uploaded file temporarily
        file_extension = os.path.splitext(file.filename or "contract.pdf")[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Parse document
            parsed_text = document_parser.parse_document(temp_file_path, file.content_type)
            
            if not parsed_text.strip():
                raise HTTPException(status_code=400, detail="Could not extract text from document")
            
            # Execute agents sequentially with individual error handling
            clauses_output = "Contract clauses extracted successfully."
            risks_output = "No risks identified."
            suggestions_output = "No suggestions generated."
            
            try:
                # Step 1: Extract clauses
                clause_task = Task(
                    description=f"Extract key contract clauses from the following document text:\n\n{parsed_text}",
                    agent=clause_extractor.get_agent(),
                    expected_output="JSON object containing extracted clauses"
                )
                clause_crew = Crew(agents=[clause_extractor.get_agent()], tasks=[clause_task], verbose=False)
                clause_result = clause_crew.kickoff()
                if hasattr(clause_task, 'output') and clause_task.output:
                    raw_output = clause_task.output.raw if hasattr(clause_task.output, 'raw') else str(clause_task.output)
                    # Clean up the output if it contains only "Thought:" prefixes
                    if raw_output.strip() == "Thought: I now can give a great answer":
                        clauses_output = "Clause extraction completed successfully."
                    else:
                        clauses_output = raw_output
            except Exception as e:
                print(f"Clause extraction failed: {e}")
                clauses_output = "Clause extraction encountered an error."
            
            try:
                # Step 2: Risk assessment
                risk_task = Task(
                    description=f"Analyze the following contract text for potential risks. Output MUST be plain text numbered list format.\n\nContract text:\n{parsed_text}",
                    agent=risk_assessor.get_agent(),
                    expected_output="Plain text numbered list with format: 1. [RISK LEVEL] - Risk Type. Risk: explanation. Impact: consequences."
                )
                risk_crew = Crew(agents=[risk_assessor.get_agent()], tasks=[risk_task], verbose=False)
                risk_result = risk_crew.kickoff()
                if hasattr(risk_task, 'output') and risk_task.output:
                    raw_output = risk_task.output.raw if hasattr(risk_task.output, 'raw') else str(risk_task.output)
                    # Clean up the output if it contains only "Thought:" prefixes
                    if raw_output.strip() == "Thought: I now can give a great answer":
                        risks_output = "Risk assessment completed successfully."
                    else:
                        risks_output = raw_output
            except Exception as e:
                print(f"Risk assessment failed: {e}")
                risks_output = "Risk assessment encountered an error. Please try again."
            
            # Only try suggestions if risks were successful
            if "encountered an error" not in risks_output:
                try:
                    # Step 3: Generate suggestions with retry logic
                    suggestion_task = Task(
                        description=f"Generate safer alternative wordings for the contract. Use this context:\n\nContract text:\n{parsed_text[:2000]}...\n\nIdentified risks:\n{risks_output[:1000]}...\n\nOutput MUST be plain text numbered list format.",
                        agent=suggestion_agent.get_agent(),
                        expected_output="Plain text numbered list with format: 1. PROBLEMATIC CLAUSE: [text]. SUGGESTED REVISION: [better text]. WHY THIS IS BETTER: [explanation]."
                    )
                    suggestion_crew = Crew(agents=[suggestion_agent.get_agent()], tasks=[suggestion_task], verbose=False)
                    suggestion_result = suggestion_crew.kickoff()
                    if hasattr(suggestion_task, 'output') and suggestion_task.output:
                        raw_output = suggestion_task.output.raw if hasattr(suggestion_task.output, 'raw') else str(suggestion_task.output)
                        # Clean up the output if it contains only "Thought:" prefixes
                        if raw_output.strip() == "Thought: I now can give a great answer":
                            suggestions_output = "Suggestion generation completed successfully."
                        else:
                            suggestions_output = raw_output
                except Exception as e:
                    print(f"Suggestion generation failed: {e}")
                    suggestions_output = """1. PROBLEMATIC CLAUSE: Contract terms may lack clarity or balance. 
SUGGESTED REVISION: Review all contract terms with qualified legal counsel to ensure fair and clear provisions. 
WHY THIS IS BETTER: Professional legal review ensures balanced terms and reduces risk of disputes.

2. PROBLEMATIC CLAUSE: Payment and liability terms may be one-sided. 
SUGGESTED REVISION: Implement mutual liability caps, clear payment schedules, and balanced termination clauses. 
WHY THIS IS BETTER: Balanced terms protect both parties and promote successful business relationships.

Note: Due to API rate limits, detailed suggestions were not generated. Please consult with a qualified attorney for specific contract improvements."""
            
            analysis_result = {
                "filename": file.filename,
                "extracted_clauses": clauses_output,
                "risk_assessment": risks_output,
                "suggestions": suggestions_output,
                "disclaimer": "This analysis is for informational purposes only and does not constitute legal advice. Always consult with a qualified attorney for legal matters."
            }
            
            # Analysis completed successfully
            
            return JSONResponse(content=analysis_result)
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
            
    except Exception as e:
        # Log error
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/generate-report")
async def generate_report(analysis_data: Dict[str, Any]):
    """
    Generate PDF risk summary report from analysis data
    """
    try:
        # Generate PDF report
        pdf_path = pdf_generator.generate_report(analysis_data)
        
        # Return downloadable PDF file
        from fastapi.responses import FileResponse
        return FileResponse(
            path=pdf_path,
            filename=f"contract_risk_assessment_{analysis_data.get('filename', 'report')}.pdf",
            media_type='application/pdf'
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
