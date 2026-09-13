import json
from datetime import datetime


class JSONExporter:
    """Exports code reviews as structured JSON"""
    
    def __init__(self, review):
        self.review = review
    
    def generate(self) -> dict:
        """Generate JSON export"""
        return {
            'review': {
                'id': self.review.id,
                'filename': self.review.filename,
                'language': self.review.language,
                'code_content': self.review.code_content,
                'analysis_duration': self.review.analysis_duration,
                'created_at': self.review.created_at.isoformat(),
                'updated_at': self.review.updated_at.isoformat(),
            },
            'scores': {
                'overall': self.review.quality_score,
                'security': self.review.security_score,
                'reliability': self.review.reliability_score,
                'maintainability': self.review.maintainability_score,
                'complexity': self.review.complexity_score,
            },
            'summary': {
                'bug_count': self.review.bug_count,
                'security_count': self.review.security_count,
                'suggestion_count': self.review.suggestion_count,
            },
            'issues': [
                {
                    'id': issue.id,
                    'type': issue.type,
                    'severity': issue.severity,
                    'category': issue.category,
                    'line_number': issue.line_number,
                    'end_line_number': issue.end_line_number,
                    'title': issue.title,
                    'description': issue.description,
                    'explanation': issue.explanation,
                    'impact': issue.impact,
                    'suggested_fix': issue.suggested_fix,
                    'cwe': issue.cwe,
                    'cwe_url': issue.cwe_url,
                    'code_context': issue.code_context,
                }
                for issue in self.review.issues
            ],
            'metadata': {
                'exported_at': datetime.utcnow().isoformat(),
                'exported_by': 'Code Review Bot',
                'version': '1.0',
            }
        }
