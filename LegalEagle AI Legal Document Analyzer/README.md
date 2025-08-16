# AI Legal Document Analyzer

A sophisticated multi-agent AI system for analyzing legal contracts, identifying risks, and generating professional assessment reports.

## 🚀 Features

- **Multi-Agent AI Analysis**: Three specialized agents for comprehensive contract review
  - 📄 **ClauseExtractorAgent**: Identifies and extracts key contract provisions
  - ⚠️ **RiskAssessmentAgent**: Evaluates clauses for potential risks and red flags
  - 💡 **SuggestionAgent**: Provides safer alternative wordings for risky clauses

- **Document Support**: Upload and analyze PDF or DOCX legal contracts
- **Professional Reports**: Generate downloadable PDF risk summary reports
- **Advanced Observability**: Complete analysis tracking with Langfuse integration
- **User-Friendly Interface**: Clean Streamlit dashboard for easy interaction

## 🛠 Technology Stack

- **Backend**: FastAPI with async processing
- **Frontend**: Streamlit web interface
- **AI Orchestration**: CrewAI multi-agent framework
- **LLM**: Groq API for fast, accurate analysis
- **Document Processing**: PyMuPDF (PDF) and docx2txt (DOCX)
- **Report Generation**: ReportLab for professional PDFs
- **Observability**: Langfuse for comprehensive logging

## 📋 Prerequisites

- Python 3.8 or higher
- Groq API key ([Get one here](https://groq.com/))
- Langfuse account ([Sign up here](https://langfuse.com/))

## 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-legal-document-analyzer
   
