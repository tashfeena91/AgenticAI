# Startup Pitch Evaluator using CrewAI and Langfuse

This project implements a startup pitch evaluator using AI agents powered by CrewAI. The main goal is to provide insights and feedback on startup ideas from an investor's perspective. It leverages AI agents to research relevant market trends and then uses these trends, along with the provided pitch text, to simulate realistic investor feedback.

## Features

- **AI Agents**: Two specialized CrewAI agents for market research and pitch evaluation
- **External Integrations**: DuckDuckGo Search for market trends and Groq API for investor feedback simulation
- **Observability**: Langfuse integration for tracing and monitoring agent execution

## Architecture

### Agents (CrewAI)
- **MarketAnalystAgent**: Identifies relevant market trends.
- **PitchEvaluatorAgent**: Evaluates pitches based on market trends and provides investor feedback.

### External APIs
- **DuckDuckGo Search**: Tool for fetching real-time market trends.
- **Groq API**: LLM processing (using meta-llama/llama-4-scout-17b-16e-instruct model) for simulating investor feedback.
- **Langfuse**: Observability, logging, and tracing of agent executions.

## Getting Started

### Prerequisites
- Python 3.10+ (or compatible)
- API keys for Groq and Langfuse

### Environment Variables
The project requires API keys for Langfuse and Groq. You can set these up using Colab Secrets or directly in your environment.

*   **Using Colab Secrets:**
    If running in Google Colab, use the "Secrets" tab in the left sidebar to securely store your keys. Add the following secrets:
    *   `Langfuse_public`: Your Langfuse public key.
    *   `Langfuse_secret`: Your Langfuse secret key.
    *   `groqkey`: Your Groq API key.

*   **Setting Directly in Environment:**
    Alternatively, you can set these environment variables before running the script (e.g., in your terminal or script):
