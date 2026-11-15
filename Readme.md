# Local AI Assistant

A simple AI assistant built using Python, Ollama, and the OpenAI Python SDK.

## Technologies Used
- Python
- Ollama
- Qwen3 4B
- OpenAI Python SDK
- Python-dotenv

## Setup Instructions

### 1. Clone the repository
```bash
git clone YOUR_REPOSITORY_URL
cd Advanced-AI
```

### 2. Create virtual environment
```bash
python -m venv .venv
```

### 3. Activate virtual environment (Windows)
```cmd
.venv\Scripts\activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Install and run Ollama

Download Ollama and pull the model:

```bash
ollama pull qwen3:4b
```

### 6. Configure environment variables

Copy `.env.example` to `.env`.

### 7. Run the project
```bash
python simple_ai_assistant.py
```

## Project Description

This project connects a locally running Ollama model to Python through its OpenAI-compatible API and generates responses to user prompts.
