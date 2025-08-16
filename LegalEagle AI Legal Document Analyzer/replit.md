# Overview

This is an AI Legal Document Analyzer that leverages a multi-agent AI system to analyze legal contracts, identify risks, and generate professional assessment reports. The application allows users to upload PDF or DOCX legal documents and receive comprehensive analysis through three specialized AI agents: a ClauseExtractorAgent for identifying key contract provisions, a RiskAssessmentAgent for evaluating potential risks and red flags, and a SuggestionAgent for providing safer alternative contract wordings. The system generates downloadable PDF risk summary reports and includes complete observability through Langfuse integration.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Streamlit Web Interface**: Simple dashboard for document upload and report display with custom CSS styling for professional appearance
- **File Upload Support**: Handles PDF and DOCX contract documents through web interface
- **Real-time Analysis Display**: Shows analysis results and risk assessments in organized sections

## Backend Architecture
- **FastAPI Framework**: Asynchronous API server handling document processing and analysis requests
- **Multi-Agent AI System**: CrewAI orchestration framework managing three specialized agents:
  - ClauseExtractorAgent: Extracts key contractual clauses (parties, dates, payment terms, etc.)
  - RiskAssessmentAgent: Identifies and categorizes risks (high/medium/low) with detailed explanations
  - SuggestionAgent: Provides safer alternative wordings for risky clauses
- **Document Processing Pipeline**: Async processing workflow from upload to analysis to report generation
- **CORS Middleware**: Enables cross-origin requests for frontend-backend communication

## AI and LLM Integration
- **Groq API**: Fast LLM inference using llama3-8b-8192 model for agent responses
- **Temperature Settings**: Optimized for each agent (0.1 for extraction, 0.2 for risk assessment, 0.3 for suggestions)
- **Agent Orchestration**: CrewAI framework coordinates multi-agent workflows with specialized roles and backstories

## Document Processing
- **PDF Parsing**: PyMuPDF (fitz) for extracting text from PDF contracts
- **DOCX Parsing**: docx2txt library for Word document text extraction
- **Content Type Detection**: Automatic file type identification and appropriate parser selection
- **Error Handling**: Comprehensive error management for unsupported formats and parsing failures

## Report Generation
- **Professional PDF Reports**: ReportLab library creates structured risk assessment documents
- **Custom Styling**: Professional layout with custom colors, fonts, and formatting
- **Risk Categorization**: Visual distinction between high, medium, and low-risk clauses
- **Downloadable Output**: Generated reports available for immediate download

## Observability and Monitoring
- **Langfuse Integration**: Complete analysis tracking and logging for all agent interactions
- **Performance Monitoring**: Tracks processing times, success rates, and error patterns
- **Audit Trail**: Maintains records of all document analyses for compliance and review

## Data Flow Architecture
1. Document upload through Streamlit frontend
2. FastAPI backend receives and validates file
3. Document parser extracts text based on file type
4. Multi-agent system processes text through three specialized agents
5. Results aggregated and formatted for report generation
6. PDF report created with professional formatting
7. All steps logged to Langfuse for observability

# External Dependencies

## AI and Machine Learning Services
- **Groq API**: Primary LLM service for fast contract analysis using llama3-8b-8192 model
- **Langfuse**: Observability platform for tracking AI agent interactions and performance monitoring

## Document Processing Libraries
- **PyMuPDF (fitz)**: PDF document parsing and text extraction
- **docx2txt**: Microsoft Word document text extraction

## Web Framework and UI
- **FastAPI**: Modern async web framework for API endpoints
- **Streamlit**: Frontend framework for rapid web application development
- **Uvicorn**: ASGI server for running FastAPI applications

## AI Orchestration
- **CrewAI**: Multi-agent framework for coordinating specialized AI agents
- **LangChain Groq**: Integration layer for Groq LLM services

## Report Generation
- **ReportLab**: Professional PDF generation library for creating formatted risk assessment reports

## Environment and Configuration
- **python-dotenv**: Environment variable management for API keys and configuration
- **CORS Middleware**: Cross-origin resource sharing for frontend-backend communication

## File Handling
- **tempfile**: Temporary file management for uploaded documents
- **base64**: File encoding for frontend-backend transfer