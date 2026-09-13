import time
from typing import Dict, Any, List, Tuple
from analyzer.static_analyzer import StaticAnalyzer
from analyzer.security_scanner import SecurityScanner
from analyzer.quality_scorer import QualityScorer
from analyzer.claude_reviewer import ClaudeReviewer


class CodeAnalysisOrchestrator:
    """Orchestrates the complete code analysis pipeline"""
    
    SUPPORTED_LANGUAGES = [
        'Python',
        'JavaScript',
        'TypeScript',
        'Java',
        'C++',
        'C#',
        'Go',
        'Ruby',
        'PHP',
    ]
    
    def __init__(self, code: str, filename: str, language: str = None):
        self.code = code
        self.filename = filename
        self.language = language or self._detect_language(filename)
        self.analysis_steps = []
    
    def analyze(self) -> Dict[str, Any]:
        """Run complete analysis pipeline"""
        start_time = time.time()
        
        # Step 1: Static Analysis
        self.analysis_steps.append("Parsing source code")
        static_issues = self._run_static_analysis()
        
        # Step 2: Security Scan
        self.analysis_steps.append("Scanning for security vulnerabilities")
        security_issues = self._run_security_scan()
        
        # Step 3: Combine issues
        all_issues = static_issues + security_issues
        
        # Step 4: Quality Scoring
        self.analysis_steps.append("Calculating quality metrics")
        quality_data = self._calculate_quality_scores(all_issues)
        
        # Step 5: Claude Review (with fallback)
        self.analysis_steps.append("Consulting AI reviewer")
        ai_review = self._get_ai_review(all_issues)
        
        # Step 6: Compile results
        self.analysis_steps.append("Generating final report")
        
        analysis_duration = time.time() - start_time
        
        results = {
            'filename': self.filename,
            'language': self.language,
            'code_content': self.code,
            'analysis_duration': round(analysis_duration, 2),
            'analysis_steps': self.analysis_steps,
            
            # Issues
            'issues': all_issues,
            'bug_count': len([i for i in all_issues if i['type'] == 'bug']),
            'security_count': len([i for i in all_issues if i['type'] == 'security']),
            'quality_count': len([i for i in all_issues if i['type'] == 'quality']),
            'suggestion_count': len([i for i in all_issues if i['type'] == 'suggestion']),
            
            # Scores
            'quality_score': quality_data['overall_score'],
            'security_score': quality_data['security_score'],
            'reliability_score': quality_data['reliability_score'],
            'maintainability_score': quality_data['maintainability_score'],
            'complexity_score': quality_data['complexity_score'],
            'code_metrics': quality_data['code_metrics'],
            'score_explanation': quality_data['explanations'],
            
            # AI Review
            'ai_review': ai_review,
        }
        
        return results
    
    def _detect_language(self, filename: str) -> str:
        """Detect language from filename extension"""
        extension_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.tsx': 'TypeScript',
            '.jsx': 'JavaScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.cc': 'C++',
            '.cxx': 'C++',
            '.c': 'C',
            '.h': 'C',
            '.cs': 'C#',
            '.go': 'Go',
            '.rb': 'Ruby',
            '.php': 'PHP',
        }
        
        for ext, lang in extension_map.items():
            if filename.lower().endswith(ext):
                return lang
        
        return 'Unknown'
    
    def _run_static_analysis(self) -> List[Dict[str, Any]]:
        """Run static analysis"""
        try:
            analyzer = StaticAnalyzer(self.code, self.language)
            issues = analyzer.analyze()
            return issues
        except Exception as e:
            print(f"Static analysis error: {str(e)}")
            return []
    
    def _run_security_scan(self) -> List[Dict[str, Any]]:
        """Run security vulnerability scan"""
        try:
            scanner = SecurityScanner(self.code, self.language)
            issues = scanner.scan()
            return issues
        except Exception as e:
            print(f"Security scan error: {str(e)}")
            return []
    
    def _calculate_quality_scores(self, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate quality scores"""
        try:
            scorer = QualityScorer(self.code, issues)
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
        except Exception as e:
            print(f"Quality scoring error: {str(e)}")
            return {
                'overall_score': 50,
                'security_score': 50,
                'reliability_score': 50,
                'maintainability_score': 50,
                'complexity_score': 50,
                'code_metrics': {},
                'explanations': {},
            }
    
    def _get_ai_review(self, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get AI-powered review from Claude"""
        try:
            reviewer = ClaudeReviewer(self.code, self.language, issues)
            review = reviewer.review()
            return review
        except Exception as e:
            print(f"AI review error: {str(e)}")
            # Return empty review structure on error
            return {
                'summary': 'AI review unavailable',
                'key_strengths': [],
                'main_concerns': [],
                'refactoring_suggestions': [],
                'best_practices': [],
                'overall_assessment': 'AI review service is temporarily unavailable',
                'fallback': True,
                'error': str(e)
            }
    
    @staticmethod
    def is_language_supported(language: str) -> bool:
        """Check if language is supported"""
        return language in CodeAnalysisOrchestrator.SUPPORTED_LANGUAGES
