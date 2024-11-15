from .github_service import GitHubService
from ..models import TaskStatus, AnalysisResult
import json
from .ollama_service import OllamaService

class CodeAnalyzer:
    def __init__(self, model_name: str = "llama3.1:8b"):
        self.github_service = GitHubService()
        self.ollama_service = OllamaService(model_name)

    def analyze_pr(self, repo_url: str, pr_number: int, github_token: str = None) -> dict:
        try:
            if github_token:
                self.github_service = GitHubService(github_token)
            
            files = self.github_service.get_pr_files(repo_url, pr_number)
            
            analysis_results = []
            total_issues = 0
            critical_issues = 0
            
            for file in files:
                analysis = self.ollama_service.analyze_code(
                    file["name"],
                    file["content"]
                )
                
                issues = analysis.get("issues", [])
                
                critical_issues += sum(1 for issue in issues if issue["type"] == "bug")
                total_issues += len(issues)
                
                analysis_results.append({
                    "name": file["name"],
                    "issues": issues
                })
            
            return {
                "status": TaskStatus.COMPLETED.value,
                "results": {
                    "files": analysis_results,
                    "summary": {
                        "total_files": len(files),
                        "total_issues": total_issues,
                        "critical_issues": critical_issues
                    }
                }
            }
            
        except Exception as e:
            print(f"Error in analyze_pr: {str(e)}")
            return {
                "status": TaskStatus.FAILED.value,
                "results": {"error": str(e)}
            }