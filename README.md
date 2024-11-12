# Autonomous Code Review Agent

An AI-powered code review system that automatically analyzes GitHub pull requests and provides detailed feedback using Google's Gemini LLM.

## Features

- Asynchronous processing of GitHub PRs using Celery
- Integration with Ollama (llama3.1) for intelligent code analysis
- RESTful API built with FastAPI
- Redis-based task queue and result storage
- Comprehensive code analysis including:
  - Code style and formatting issues
  - Potential bugs and errors
  - Performance improvements
  - Best practices recommendations

## Setup Instructions

1. Clone the repository:
  
  ```bash
  git clone <repository-url>
  cd code-review-agent
  ```
  
2. Install dependencies:
  
  ```bash
  pip install -r requirements.txt
  ```
  
3. Configure environment variables:
  
  ```bash
  cp .env.example .env
  # Edit .env with your credentials
  ```
  
4. Start Redis:
  
  ```bash
  docker run -d -p 6379:6379 redis
  ```
  
5. Start Celery worker:
  
  ```bash
  celery -A app.celery_app worker --loglevel=info
  ```
  
6. Run the FastAPI application:
  
  ```bash
  uvicorn app.main:app --reload
  ```
  

## API Documentation

### POST /analyze-pr

Initiates a code review for a GitHub PR.

Request body:

```json
{
  "repo_url": "https://github.com/user/repo",
  "pr_number": 123,
  "github_token": "optional_token"
}
```

Response:

```json
{
  "task_id": "abc123"
}
```

### GET /status/{task_id}

Check the status of an analysis task.

Response:

```json
{
  "task_id": "abc123",
  "status": "processing"
}
```

### GET /results/{task_id}

Get the analysis results.

Response:

```json
{
  "task_id": "abc123",
  "status": "completed",
  "results": {
    "files": [...],
    "summary": {
      "total_files": 1,
      "total_issues": 2,
      "critical_issues": 1
    }
  }
}
```

## Output

### Analyze 

![output/analyze.png]

### Status

![output/status.png]

### Result

![output/result.png]