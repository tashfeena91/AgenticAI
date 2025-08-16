
# Symptom Checker & Doctor Prep Bot

An AI-powered medical symptom analysis tool that helps users organize their symptoms and prepare for doctor visits.

## Features

- **Streamlit Web UI**: User-friendly interface for symptom input and analysis
- **FastAPI Backend**: Secure REST API with authentication
- **AI Agents**: Three specialized CrewAI agents for symptom interpretation, condition mapping, and doctor note creation
- **External Integrations**: Groq API for LLM processing and Langfuse for observability
- **Comprehensive Analysis**: Structured symptom extraction, condition mapping, and professional doctor visit summaries

## Architecture

### Agents (CrewAI)
- **SymptomInterpreterAgent**: Extracts structured information from user input
- **ConditionMapperAgent**: Maps symptoms to potential medical considerations
- **DoctorNoteAgent**: Creates professional summaries for doctor visits

### External APIs
- **Groq API**: LLM processing with Llama3-8B model
- **Langfuse**: Observability, logging, and tracing

### Security
- API key authentication for backend endpoints
- CORS configuration for cross-origin requests
- Input validation and error handling

## Getting Started

### Prerequisites
- Python 3.11+
- API keys for Groq and Langfuse

### Environment Variables
Create a `.env` file with:
```
Langfuse_secretkey=your_langfuse_secret_key
Langfuse_publickey=your_langfuse_public_key
Groq_key=your_groq_api_key
API_KEY=your_api_key_for_backend
```

### Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### Streamlit UI
```bash
streamlit run streamlit_app.py --server.address=0.0.0.0 --server.port=5000
```

#### FastAPI Backend
```bash
uvicorn api.main:app --host 0.0.0.0 --port=8000 --reload
```

#### Docker Deployment
```bash
docker-compose up
```

## API Endpoints

### Authentication
All API endpoints require Bearer token authentication:
```
Authorization: Bearer your_api_key
```

### Endpoints
- `GET /health` - Health check
- `POST /analyze-symptoms` - Complete symptom analysis
- `POST /interpret-symptoms` - Symptom interpretation only
- `GET /docs` - API documentation (Swagger UI)

## Usage Example

### Web Interface
1. Visit the Streamlit app
2. Enter your symptoms in the text area or use the guided form
3. Click "Analyze Symptoms" to get structured analysis
4. Download the summary for your doctor visit

### API Usage
```python
import requests

headers = {"Authorization": "Bearer your_api_key"}
data = {"symptoms": "I have a headache for 3 days with nausea"}

response = requests.post(
    "http://localhost:8000/analyze-symptoms",
    json=data,
    headers=headers
)
```

## Observability

The application uses Langfuse for comprehensive observability:
- Request tracing across all agents
- Performance monitoring
- Error tracking
- Usage analytics

## Deployment

### Replit Deployment
The app is configured for easy deployment on Replit with:
- Streamlit workflow on port 5000
- FastAPI workflow on port 8000
- Environment variable management

### Docker Deployment
Use the provided Docker configuration:
- Multi-service setup with docker-compose
- Separate containers for API and UI
- Environment variable injection

## Medical Disclaimer

⚠️ **IMPORTANT**: This tool is NOT a diagnostic tool and does not replace professional medical advice. Always consult healthcare professionals for proper diagnosis and treatment.

## License

This project is for educational purposes. Please ensure compliance with medical regulations in your jurisdiction.
