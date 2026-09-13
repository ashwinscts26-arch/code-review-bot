import time
from datetime import datetime
from typing import Dict, Any, List, Tuple
from models import db, Review, Issue
from analyzer.static_analyzer import StaticAnalyzer
from analyzer.security_scanner import SecurityScanner
from analyzer.quality_scorer import QualityScorer
from analyzer.claude_reviewer import ClaudeReviewer


class ReviewService:
    """Orchestrates the complete code review process"""
    
    @staticmethod
    def create_review(filename: str, code: str, language: str) -> Tuple[Review, Dict[str, Any]]:
        """Create a new review and return the review object and metadata"""
        start_time = time.time()
        
        # Run analysis pipeline
        static_issues = ReviewService._run_static_analysis(code, language)
        security_issues = ReviewService._run_security_analysis(code, language)
        all_issues = static_issues + security_issues
        
        # Calculate quality scores
        scorer = QualityScorer(code, all_issues)
        scores = scorer.calculate_scores()
        
        # Get AI review
        reviewer = ClaudeReviewer(code, language, all_issues)
        ai_review = reviewer.review()
        
        # Calculate analysis duration
        analysis_duration = time.time() - start_time
        
        # Create review in database
        review = Review(
            filename=filename,
            language=language,
            code_content=code,
            quality_score=scores['overall_score'],
            security_score=scores['security_score'],
            reliability_score=scores['reliability_score'],
            maintainability_score=scores['maintainability_score'],
            complexity_score=scores['complexity_score'],
            bug_count=len([i for i in all_issues if i['type'] == 'bug']),
            security_count=len([i for i in all_issues if i['type'] == 'security']),
            suggestion_count=len([i for i in all_issues if i['type'] == 'suggestion']),
            analysis_duration=analysis_duration,
        )
        
        # Add issues to review
        for issue_data in all_issues:
            issue = Issue(
                type=issue_data['type'],
                severity=issue_data['severity'],
                category=issue_data['category'],
                line_number=issue_data['line_number'],
                end_line_number=issue_data.get('end_line_number'),
                title=issue_data['title'],
                description=issue_data['description'],
                explanation=issue_data.get('explanation'),
                impact=issue_data.get('impact'),
                suggested_fix=issue_data.get('suggested_fix'),
                cwe=issue_data.get('cwe'),
                cwe_url=issue_data.get('cwe_url'),
                code_context=issue_data.get('code_context'),
            )
            review.issues.append(issue)
        
        # Save to database
        db.session.add(review)
        db.session.commit()
        
        # Prepare response metadata
        metadata = {
            'analysis_duration': analysis_duration,
            'ai_review': ai_review,
            'score_explanation': scorer.get_score_explanation(scores),
            'code_metrics': scores['code_metrics'],
        }
        
        return review, metadata
    
    @staticmethod
    def _run_static_analysis(code: str, language: str) -> List[Dict[str, Any]]:
        """Run static analysis on code"""
        try:
            analyzer = StaticAnalyzer(code, language)
            return analyzer.analyze()
        except Exception as e:
            print(f"Static analysis error: {str(e)}")
            return []
    
    @staticmethod
    def _run_security_analysis(code: str, language: str) -> List[Dict[str, Any]]:
        """Run security analysis on code"""
        try:
            scanner = SecurityScanner(code, language)
            return scanner.scan()
        except Exception as e:
            print(f"Security analysis error: {str(e)}")
            return []
    
    @staticmethod
    def get_review_by_id(review_id: int) -> Dict[str, Any]:
        """Get a review by ID with all details"""
        review = Review.query.get(review_id)
        if not review:
            return None
        return review.to_dict()
    
    @staticmethod
    def get_all_reviews(limit: int = 50, offset: int = 0) -> Tuple[List[Dict[str, Any]], int]:
        """Get paginated list of all reviews"""
        query = Review.query.order_by(Review.created_at.desc())
        total = query.count()
        reviews = query.limit(limit).offset(offset).all()
        return [r.to_dict() for r in reviews], total
    
    @staticmethod
    def delete_review(review_id: int) -> bool:
        """Delete a review"""
        review = Review.query.get(review_id)
        if review:
            db.session.delete(review)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_analytics() -> Dict[str, Any]:
        """Get analytics about all reviews"""
        all_reviews = Review.query.all()
        
        if not all_reviews:
            return {
                'total_reviews': 0,
                'average_quality_score': 0,
                'total_bugs': 0,
                'total_security_issues': 0,
                'language_distribution': {},
                'severity_distribution': {},
            }
        
        total_score = sum(r.quality_score for r in all_reviews)
        total_bugs = sum(r.bug_count for r in all_reviews)
        total_security = sum(r.security_count for r in all_reviews)
        
        # Language distribution
        language_dist = {}
        for review in all_reviews:
            language_dist[review.language] = language_dist.get(review.language, 0) + 1
        
        # Severity distribution
        severity_dist = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'info': 0}
        all_issues = Issue.query.all()
        for issue in all_issues:
            severity_dist[issue.severity] = severity_dist.get(issue.severity, 0) + 1
        
        return {
            'total_reviews': len(all_reviews),
            'average_quality_score': int(total_score / len(all_reviews)),
            'total_bugs': total_bugs,
            'total_security_issues': total_security,
            'language_distribution': language_dist,
            'severity_distribution': severity_dist,
            'score_trend': ReviewService._get_score_trend(all_reviews),
        }
    
    @staticmethod
    def _get_score_trend(reviews: List[Review]) -> List[Dict[str, Any]]:
        """Get quality score trend over time"""
        # Sort by date
        sorted_reviews = sorted(reviews, key=lambda r: r.created_at)
        
        trend = []
        for review in sorted_reviews[-10:]:  # Last 10 reviews
            trend.append({
                'date': review.created_at.strftime('%Y-%m-%d'),
                'score': review.quality_score,
                'filename': review.filename,
            })
        
        return trend
