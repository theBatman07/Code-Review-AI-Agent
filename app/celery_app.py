from celery import Celery
from .config import settings
from .services.code_analyzer import CodeAnalyzer

celery_app = Celery(
    "code_review",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend
)

@celery_app.task
def analyze_pr_task(repo_url: str, pr_number: int, github_token: str = None) -> dict:
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_pr(repo_url, pr_number, github_token)
    # Add task_id to the result
    result['task_id'] = analyze_pr_task.request.id
    return result