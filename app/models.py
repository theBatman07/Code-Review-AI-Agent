from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class PRRequest(BaseModel):
    repo_url: str
    pr_number: int
    github_token: Optional[str] = None

class CodeIssue(BaseModel):
    type: str
    line: int
    description: str
    suggestion: str

class FileAnalysis(BaseModel):
    name: str
    issues: List[CodeIssue]

class AnalysisSummary(BaseModel):
    total_files: int
    total_issues: int
    critical_issues: int

class AnalysisResult(BaseModel):
    task_id: str
    status: TaskStatus
    results: Optional[Dict] = None

    def dict(self, *args, **kwargs):
        # Convert to dictionary and ensure all nested objects are serializable
        d = super().dict(*args, **kwargs)
        if isinstance(d['status'], TaskStatus):
            d['status'] = d['status'].value
        return d