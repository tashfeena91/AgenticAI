import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import tempfile
import base64

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="AI Legal Document Analyzer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
    }
    .disclaimer {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        color: #856404;
    }
    .risk-high {
        color: #dc3545;
        font-weight: bold;
    }
    .risk-medium {
        color: #fd7e14;
        font-weight: bold;
    }
    .risk-low {
        color: #28a745;
        font-weight: bold;
    }
    .clause-box {
        background-color: #f8f9fa;
        border-left: 4px solid #007bff;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# FastAPI backend URL
BACKEND_URL = "http://localhost:8000"

def main():
    st.markdown('<h1 class="main-header">⚖️ AI Legal Document Analyzer</h1>', unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("""
    <div class="disclaimer">
        <strong>⚠️ Important Legal Disclaimer:</strong> This tool is for informational purposes only and does not constitute legal advice. 
        The analysis provided should not be relied upon for legal decisions. Always consult with a qualified attorney for legal matters.
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Analysis Options")
        st.info("Upload a legal contract in PDF or DOCX format to get started.")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a contract file",
            type=['pdf', 'docx'],
            help="Supported formats: PDF, DOCX"
        )
        
        if uploaded_file:
            st.success(f"File uploaded: {uploaded_file.name}")
            st.write(f"File size: {len(uploaded_file.getvalue())} bytes")
    
    # Main content area
    if uploaded_file is not None:
        col1, col2 = st.columns([3, 1])
        
        with col2:
            analyze_button = st.button("🔍 Analyze Contract", type="primary")
        
        if analyze_button:
            with st.spinner("🤖 AI agents are analyzing your contract..."):
                try:
                    # Prepare file for upload
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    
                    # Make request to backend
                    response = requests.post(f"{BACKEND_URL}/analyze-contract", files=files)
                    
                    if response.status_code == 200:
                        analysis_result = response.json()
                        display_analysis_results(analysis_result)
                    else:
                        st.error(f"Analysis failed: {response.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend service. Please ensure the FastAPI server is running on port 8000.")
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
    
    else:
        # Welcome message
        st.markdown("""
        ## 🚀 Welcome to AI Legal Document Analyzer
        
        This powerful tool uses advanced AI agents to analyze legal contracts and provide comprehensive risk assessments:
        
        ### 🤖 Our AI Agents:
        - **📄 Clause Extractor Agent**: Identifies and extracts key contract provisions
        - **⚠️ Risk Assessment Agent**: Evaluates clauses for potential risks and red flags  
        - **💡 Suggestion Agent**: Provides safer alternative wordings for risky clauses
        
        ### 📊 What You'll Get:
        - Detailed clause extraction and categorization
        - Risk severity analysis with explanations
        - Professional PDF risk summary report
        - Suggested improvements for high-risk provisions
        
        ### 🔒 Privacy & Security:
        - Your documents are processed securely
        - No data is permanently stored
        - All analysis is performed in real-time
        
        **Ready to get started?** Upload your contract using the sidebar! 📤
        """)

def display_analysis_results(analysis_result):
    """Display the contract analysis results"""
    
    st.success("✅ Analysis completed successfully!")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Extracted Clauses", "⚠️ Risk Assessment", "💡 Suggestions", "📊 Summary Report"])
    
    with tab1:
        st.header("📄 Extracted Contract Clauses")
        
        if 'extracted_clauses' in analysis_result:
            clauses = analysis_result['extracted_clauses']
            
            # Display clauses in organized sections
            if isinstance(clauses, str):
                try:
                    clauses = json.loads(clauses)
                except:
                    st.write(clauses)
            
            if isinstance(clauses, dict):
                for clause_type, clause_content in clauses.items():
                    st.markdown(f"""
                    <div class="clause-box">
                        <h4>{clause_type.replace('_', ' ').title()}</h4>
                        <p>{clause_content}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write(clauses)
        else:
            st.info("No clauses extracted. This might indicate an issue with document parsing.")
    
    with tab2:
        st.header("⚠️ Risk Assessment")
        
        if 'risk_assessment' in analysis_result:
            risks = analysis_result['risk_assessment']
            
            if isinstance(risks, str):
                try:
                    risks = json.loads(risks)
                except:
                    st.write(risks)
            
            if isinstance(risks, dict):
                for risk_item, risk_details in risks.items():
                    if isinstance(risk_details, dict) and 'severity' in risk_details:
                        severity = risk_details['severity'].lower()
                        if severity == 'high':
                            st.markdown(f'<p class="risk-high">🔴 HIGH RISK: {risk_item}</p>', unsafe_allow_html=True)
                        elif severity == 'medium':
                            st.markdown(f'<p class="risk-medium">🟡 MEDIUM RISK: {risk_item}</p>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<p class="risk-low">🟢 LOW RISK: {risk_item}</p>', unsafe_allow_html=True)
                        
                        if 'explanation' in risk_details:
                            st.write(f"**Explanation:** {risk_details['explanation']}")
                    else:
                        st.write(f"**{risk_item}:** {risk_details}")
                    st.write("---")
            else:
                st.write(risks)
        else:
            st.info("No risk assessment available.")
    
    with tab3:
        st.header("💡 Suggested Improvements")
        
        if 'suggestions' in analysis_result:
            suggestions = analysis_result['suggestions']
            
            if isinstance(suggestions, str):
                try:
                    suggestions = json.loads(suggestions)
                except:
                    st.write(suggestions)
            
            if isinstance(suggestions, dict):
                for suggestion_key, suggestion_content in suggestions.items():
                    st.markdown(f"### {suggestion_key.replace('_', ' ').title()}")
                    if isinstance(suggestion_content, dict):
                        if 'current' in suggestion_content:
                            st.markdown("**Current wording:**")
                            st.code(suggestion_content['current'])
                        if 'suggested' in suggestion_content:
                            st.markdown("**Suggested improvement:**")
                            st.code(suggestion_content['suggested'])
                        if 'rationale' in suggestion_content:
                            st.markdown(f"**Rationale:** {suggestion_content['rationale']}")
                    else:
                        st.write(suggestion_content)
                    st.write("---")
            else:
                st.write(suggestions)
        else:
            st.info("No suggestions available.")
    
    with tab4:
        st.header("📊 Executive Summary & Report")
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Document", analysis_result.get('filename', 'Unknown'))
        
        with col2:
            # Count risks (simplified)
            risk_count = len(analysis_result.get('risk_assessment', {})) if isinstance(analysis_result.get('risk_assessment', {}), dict) else 0
            st.metric("Risks Identified", risk_count)
        
        with col3:
            # Count suggestions (simplified)
            suggestion_count = len(analysis_result.get('suggestions', {})) if isinstance(analysis_result.get('suggestions', {}), dict) else 0
            st.metric("Suggestions Made", suggestion_count)
        
        # Generate PDF Report button
        if st.button("📄 Generate PDF Report", type="secondary"):
            with st.spinner("Generating PDF report..."):
                try:
                    report_response = requests.post(f"{BACKEND_URL}/generate-report", json=analysis_result)
                    if report_response.status_code == 200:
                        st.success("✅ PDF report generated successfully!")
                        st.info("💾 In a production environment, the PDF would be available for download here.")
                    else:
                        st.error("Failed to generate PDF report")
                except Exception as e:
                    st.error(f"Error generating report: {str(e)}")
        
        # Display disclaimer
        st.markdown("""
        <div class="disclaimer">
            <strong>📋 Analysis Summary:</strong> This automated analysis has identified potential areas of concern in your contract. 
            Please review all findings carefully and consult with a qualified attorney before making any legal decisions.
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
