from typing import List, Dict, Any


class QualityScorer:
    """Calculates code quality scores based on analysis results"""
    
    def __init__(self, code: str, issues: List[Dict[str, Any]]):
        self.code = code
        self.issues = issues
        self.lines = code.split('\n')
        self.total_lines = len(self.lines)
    
    def calculate_scores(self) -> Dict[str, Any]:
        """Calculate overall and category-specific quality scores"""
        
        # Initialize scores
        scores = {
            'security_score': 100,
            'reliability_score': 100,
            'maintainability_score': 100,
            'complexity_score': 100,
        }
        
        # Deduct points for issues
        for issue in self.issues:
            severity_points = self._get_severity_points(issue['severity'])
            
            if issue['type'] == 'security':
                scores['security_score'] -= severity_points
            elif issue['type'] == 'bug':
                scores['reliability_score'] -= severity_points
            elif issue['type'] == 'quality':
                if issue.get('category') == 'Function Too Long':
                    scores['complexity_score'] -= severity_points
                else:
                    scores['maintainability_score'] -= severity_points
            elif issue['type'] == 'suggestion':
                scores['maintainability_score'] -= severity_points // 2
        
        # Clamp scores to 0-100
        for key in scores:
            scores[key] = max(0, min(100, scores[key]))
        
        # Calculate overall score (weighted average)
        overall_score = int(
            scores['security_score'] * 0.35 +
            scores['reliability_score'] * 0.30 +
            scores['maintainability_score'] * 0.20 +
            scores['complexity_score'] * 0.15
        )
        
        # Add code metrics
        code_metrics = self._calculate_code_metrics()
        
        return {
            'overall_score': overall_score,
            'security_score': scores['security_score'],
            'reliability_score': scores['reliability_score'],
            'maintainability_score': scores['maintainability_score'],
            'complexity_score': scores['complexity_score'],
            'code_metrics': code_metrics,
        }
    
    def _get_severity_points(self, severity: str) -> int:
        """Get point deduction for severity level"""
        severity_map = {
            'critical': 15,
            'high': 10,
            'medium': 5,
            'low': 2,
            'info': 1,
        }
        return severity_map.get(severity, 0)
    
    def _calculate_code_metrics(self) -> Dict[str, Any]:
        """Calculate code complexity and other metrics"""
        metrics = {
            'lines_of_code': self.total_lines,
            'average_line_length': sum(len(line) for line in self.lines) / max(1, self.total_lines),
            'cyclomatic_complexity_estimate': self._estimate_complexity(),
            'duplication_ratio': self._estimate_duplication(),
        }
        return metrics
    
    def _estimate_complexity(self) -> float:
        """Estimate cyclomatic complexity"""
        complexity = 1  # Base complexity
        
        # Count control flow statements
        control_keywords = ['if', 'else', 'for', 'while', 'catch', 'case', 'and', 'or']
        for line in self.lines:
            for keyword in control_keywords:
                if f' {keyword} ' in f' {line.lower()} ':
                    complexity += 1
        
        return min(complexity / self.total_lines * 100, 100)
    
    def _estimate_duplication(self) -> float:
        """Estimate code duplication ratio"""
        # Simple duplication detection: look for duplicate lines
        line_counts = {}
        for line in self.lines:
            stripped = line.strip()
            if len(stripped) > 20:  # Only count non-trivial lines
                line_counts[stripped] = line_counts.get(stripped, 0) + 1
        
        duplicate_lines = sum(count for count in line_counts.values() if count > 1)
        
        return (duplicate_lines / self.total_lines * 100) if self.total_lines > 0 else 0
    
    def get_score_explanation(self, scores: Dict[str, Any]) -> Dict[str, str]:
        """Generate explanations for score deductions"""
        explanations = {}
        
        # Security explanation
        security_deductions = 100 - scores['security_score']
        if security_deductions > 0:
            security_issues = [i for i in self.issues if i['type'] == 'security']
            explanations['security'] = f"Found {len(security_issues)} security issue(s) causing {security_deductions} point deduction"
        else:
            explanations['security'] = "No security issues found"
        
        # Reliability explanation
        reliability_deductions = 100 - scores['reliability_score']
        if reliability_deductions > 0:
            bug_issues = [i for i in self.issues if i['type'] == 'bug']
            explanations['reliability'] = f"Found {len(bug_issues)} potential bug(s) causing {reliability_deductions} point deduction"
        else:
            explanations['reliability'] = "No obvious bugs detected"
        
        # Maintainability explanation
        maintainability_deductions = 100 - scores['maintainability_score']
        if maintainability_deductions > 0:
            quality_issues = [i for i in self.issues if i['type'] == 'quality']
            explanations['maintainability'] = f"Found {len(quality_issues)} code quality issue(s) causing {maintainability_deductions} point deduction"
        else:
            explanations['maintainability'] = "Code appears well-structured and maintainable"
        
        # Complexity explanation
        complexity_deductions = 100 - scores['complexity_score']
        complexity = scores['code_metrics']['cyclomatic_complexity_estimate']
        if complexity > 50:
            explanations['complexity'] = f"High cyclomatic complexity ({complexity:.1f}) suggests code could be simplified"
        else:
            explanations['complexity'] = "Complexity is within reasonable bounds"
        
        return explanations
