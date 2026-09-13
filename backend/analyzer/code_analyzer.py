import time
import json
from typing import Dict, Any, List, Tuple
from analyzer.static_analyzer import StaticAnalyzer
from analyzer.security_scanner import SecurityScanner
from analyzer.quality_scorer import QualityScorer
from analyzer.claude_reviewer import ClaudeReviewer


class CodeAnalyzer:
    """Orchestrates code analysis pipeline"""
    
    SUPPORTED_LANGUAGES = [
        'python', 'javascript', 'typescript', 'java', 
        'cpp', 'go', 'ruby', 'csharp', 'php'
    ]
    
    def __init__(self, code: str, language: str, filename: str):
        self.code = code
        self.language = language.lower()
        self.filename = filename
        self.issues: List[Dict[str, Any]] = []
        self.analysis_duration = 0
        self.ai_review = None
        self.scores = None
    
    def analyze(self) -> Dict[str, Any]:
        """Run complete analysis pipeline"""
        start_time = time.time()
        
        # Normalize language
        self.language = self._normalize_language(self.language)
        
        # Step 1: Static Analysis
        static_issues = self._static_analysis()
        
        # Step 2: Security Scanning
        security_issues = self._security_scan()
        
        # Combine issues
        self.issues = static_issues + security_issues
        
        # Step 3: Quality Scoring
        scores = self._calculate_scores()
        
        # Step 4: AI Review
        ai_review = self._get_ai_review()
        
        # Calculate duration
        self.analysis_duration = round(time.time() - start_time, 2)
        
        # Build result
        result = {
            'filename': self.filename,
            'language': self.language,
            'code_content': self.code,
            'analysis_duration': self.analysis_duration,
            'issues': self.issues,
            'scores': scores,
            'ai_review': ai_review,
            'issue_counts': self._count_issues(),
        }
        
        return result
    
    def _normalize_language(self, language: str) -> str:
        """Normalize language name"""
        language = language.lower().strip()
        
        # Handle common aliases
        aliases = {
            'js': 'javascript',
            'ts': 'typescript',
            'py': 'python',
            'java': 'java',
            'c++': 'cpp',
            'cpp': 'cpp',
            'go': 'go',
            'rb': 'ruby',
            'cs': 'csharp',
            'php': 'php',
        }
        
        language = aliases.get(language, language)
        
        # Validate
        if language not in self.SUPPORTED_LANGUAGES:
            return 'generic'  # Fallback to generic analysis
        
        return language
    
    def _static_analysis(self) -> List[Dict[str, Any]]:
        """Run static code analysis"""
        analyzer = StaticAnalyzer(self.code, self.language)
        return analyzer.analyze()
    
    def _security_scan(self) -> List[Dict[str, Any]]:
        """Run security vulnerability scanning"""
        scanner = SecurityScanner(self.code, self.language)
        return scanner.scan()
    
    def _calculate_scores(self) -> Dict[str, Any]:
        """Calculate quality scores"""
        scorer = QualityScorer(self.code, self.issues)
        scores = scorer.calculate_scores()
        explanations = scorer.get_score_explanation(scores)
        
        return {
            'overall_score': scores['overall_score'],
            'security_score': scores['security_score'],
            'reliability_score': scores['reliability_score'],
            'maintainability_score': scores['maintainability_score'],
            'complexity_score': scores['complexity_score'],
            'code_metrics': scores['code_metrics'],
            'explanations': explanations,
        }
    
    def _get_ai_review(self) -> Dict[str, Any]:
        """Get AI-powered review from Claude"""
        reviewer = ClaudeReviewer(self.code, self.language, self.issues)
        return reviewer.review()
    
    def _count_issues(self) -> Dict[str, int]:
        """Count issues by type and severity"""
        counts = {
            'total': len(self.issues),
            'critical': len([i for i in self.issues if i.get('severity') == 'critical']),
            'high': len([i for i in self.issues if i.get('severity') == 'high']),
            'medium': len([i for i in self.issues if i.get('severity') == 'medium']),
            'low': len([i for i in self.issues if i.get('severity') == 'low']),
            'security': len([i for i in self.issues if i.get('type') == 'security']),
            'bugs': len([i for i in self.issues if i.get('type') == 'bug']),
            'quality': len([i for i in self.issues if i.get('type') == 'quality']),
            'suggestions': len([i for i in self.issues if i.get('type') == 'suggestion']),
        }
        return counts
