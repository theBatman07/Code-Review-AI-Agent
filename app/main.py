from fastapi import FastAPI, HTTPException
from .models import PRRequest, AnalysisResult, TaskStatus
from .celery_app import analyze_pr_task
from celery.result import AsyncResult

app = FastAPI(title="Code Review Agent")

@app.post("/analyze-pr")
async def analyze_pr(request: PRRequest) -> dict:
    task = analyze_pr_task.delay(
        request.repo_url,
        request.pr_number,
        request.github_token
    )
    return {"task_id": task.id}

@app.get("/status/{task_id}")
async def get_status(task_id: str) -> dict:
    task = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status.lower()
    }

@app.get("/results/{task_id}")
async def get_results(task_id: str) -> AnalysisResult:
    task = AsyncResult(task_id)
    if not task.ready():
        raise HTTPException(status_code=404, detail="Results not ready")
    
    result = task.get()
    return AnalysisResult(
        task_id=task_id,
        status=result['status'],
        results=result['results']
    )