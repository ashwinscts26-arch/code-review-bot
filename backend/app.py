import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from io import BytesIO
import tempfile

from models import db, Review, Issue, SharedLink
from analyzer.orchestrator import CodeAnalysisOrchestrator
from exports.pdf_exporter import PDFExporter
from exports.json_exporter import JSONExporter
from exports.csv_exporter import CSVExporter


# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///code_review.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size

# Initialize extensions
db.init_app(app)
CORS(app)

# Create tables
with app.app_context():
    db.create_all()


# ═══════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════════════════

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.utcnow().isoformat()})


# ═══════════════════════════════════════════════════════════════════
# CODE UPLOAD & ANALYSIS
# ═══════════════════════════════════════════════════════════════════

@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    """Upload and analyze code"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Get code from either file or paste
        code = data.get('code')
        filename = data.get('filename', 'code.txt')
        language = data.get('language')
        
        # Validation
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        if len(code) > 50000:
            return jsonify({'error': 'Code too large (max 50KB)'}), 400
        
        if len(code.strip()) < 10:
            return jsonify({'error': 'Code too short'}), 400
        
        # Run analysis
        orchestrator = CodeAnalysisOrchestrator(code, filename, language)
        results = orchestrator.analyze()
        
        # Save to database
        review = Review(
            filename=filename,
            language=results['language'],
            code_content=code,
            quality_score=results['quality_score'],
            bug_count=results['bug_count'],
            security_count=results['security_count'],
            suggestion_count=results['suggestion_count'],
            security_score=results['security_score'],
            reliability_score=results['reliability_score'],
            maintainability_score=results['maintainability_score'],
            complexity_score=results['complexity_score'],
            analysis_duration=results['analysis_duration'],
        )
        
        db.session.add(review)
        db.session.flush()  # Get the ID
        
        # Save issues
        for issue_data in results['issues']:
            issue = Issue(
                review_id=review.id,
                type=issue_data.get('type', 'bug'),
                severity=issue_data.get('severity', 'medium'),
                category=issue_data.get('category', 'General'),
                line_number=issue_data.get('line_number', 0),
                end_line_number=issue_data.get('end_line_number'),
                title=issue_data.get('title', 'Issue'),
                description=issue_data.get('description', ''),
                explanation=issue_data.get('explanation'),
                impact=issue_data.get('impact'),
                suggested_fix=issue_data.get('suggested_fix'),
                cwe=issue_data.get('cwe'),
                cwe_url=issue_data.get('cwe_url'),
                code_context=issue_data.get('code_context'),
            )
            db.session.add(issue)
        
        db.session.commit()
        
        # Return results
        return jsonify({
            'review_id': review.id,
            'filename': review.filename,
            'language': review.language,
            'quality_score': review.quality_score,
            'bug_count': review.bug_count,
            'security_count': review.security_count,
            'suggestion_count': review.suggestion_count,
            'analysis_duration': review.analysis_duration,
            'security_score': review.security_score,
            'reliability_score': review.reliability_score,
            'maintainability_score': review.maintainability_score,
            'complexity_score': review.complexity_score,
            'created_at': review.created_at.isoformat(),
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════════════════════
# RETRIEVE REVIEW
# ═══════════════════════════════════════════════════════════════════

@app.route('/api/review/<int:review_id>', methods=['GET'])
def get_review(review_id):
    """Get a specific review"""
    try:
        review = Review.query.get(review_id)
        
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        return jsonify(review.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════════════════════
# REVIEW HISTORY
# ═══════════════════════════════════════════════════════════════════

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get review history with filtering and pagination"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        language = request.args.get('language')
        min_score = request.args.get('min_score', type=int)
        search = request.args.get('search')
        
        # Build query
        query = Review.query
        
        # Apply filters
        if language:
            query = query.filter_by(language=language)
        
        if min_score is not None:
            query = query.filter(Review.quality_score >= min_score)
        
        if search:
            query = query.filter(Review.filename.ilike(f'%{search}%'))
        
        # Sort by newest first
        query = query.order_by(Review.created_at.desc())
        
        # Paginate
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page,
            'per_page': per_page,
            'reviews': [
                {
                    'id': r.id,
                    'filename': r.filename,
                    'language': r.language,
                    'quality_score': r.quality_score,
                    'bug_count': r.bug_count,
                    'security_count': r.security_count,
                    'suggestion_count': r.suggestion_count,
                    'created_at': r.created_at.isoformat(),
                }
                for r in paginated.items
            ]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════════════════════
# DELETE REVIEW
# ═══════════════════════════════════════════════════════════════════

@app.route('/api/review/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a review"""
    try:
        review = Review.query.get(review_id)
        
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        db.session.delete(review)
        db.session.commit()
        
        return jsonify({'message': 'Review deleted'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════════════════════
# STATISTICS
# ═══════════════════════════════════════════════════════════════════

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get analytics and statistics"""
    try:
        reviews = Review.query.all()
        
        if not reviews:
            return jsonify({
                'total_reviews': 0,
                'average_score': 0,
                'total_issues': 0,
                'total_bugs': 0,
                'total_security_issues': 0,
                'language_distribution': {},
                'severity_distribution': {},
            }), 200
        
        # Calculate stats
        total_reviews = len(reviews)
        average_score = sum(r.quality_score for r in reviews) / total_reviews
        
        # Count issues
        total_issues = sum(r.bug_count + r.security_count + r.suggestion_count for r in reviews)
        total_bugs = sum(r.bug_count for r in reviews)
        total_security_issues = sum(r.security_count for r in reviews)
        
        # Language distribution
        language_dist = {}
        for review in reviews:
            language_dist[review.language] = language_dist.get(review.language, 0) + 1
        
        # Severity distribution
        severity_dist = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'info': 0,
        }
        
        for review in reviews:
            for issue in review.issues:
                if issue.severity in severity_dist:
                    severity_dist[issue.severity] += 1
        
        return jsonify({
            'total_reviews': total_reviews,
            'average_score': round(average_score, 1),
            'total_issues': total_issues,
            'total_bugs': total_bugs,
            'total_security_issues': total_security_issues,
            'language_distribution': language_dist,
            'severity_distribution': severity_dist,
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════

@app.route('/api/export/<int:review_id>/pdf', methods=['GET'])
def export_pdf(review_id):
    """Export review as PDF"""
    try:
        review = Review.query.get(review_id)
        
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        exporter = PDFExporter(review)
        pdf_bytes = exporter.generate()
        
        return send_file(
            BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'{review.filename}_review.pdf'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/<int:review_id>/json', methods=['GET'])
def export_json(review_id):
    """Export review as JSON"""
    try:
        review = Review.query.get(review_id)
        
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        exporter = JSONExporter(review)
        json_data = exporter.generate()
        
        return jsonify(json_data), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/<int:review_id>/csv', methods=['GET'])
def export_csv(review_id):
    """Export review as CSV"""
    try:
        review = Review.query.get(review_id)
        
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        exporter = CSVExporter(review)
        csv_bytes = exporter.generate()
        
        return send_file(
            BytesIO(csv_bytes),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{review.filename}_review.csv'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════════════════════
# SHARING
# ═══════════════════════════════════════════════════════════════════

@app.route('/api/share/<int:review_id>', methods=['POST'])
def create_share_link(review_id):
    """Create a shareable link for a review"""
    try:
        review = Review.query.get(review_id)
        
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        # Check if share link already exists
        existing = SharedLink.query.filter_by(review_id=review_id).first()
        if existing and not existing.is_expired():
            return jsonify({
                'token': existing.token,
                'url': f'/share/{existing.token}',
                'created_at': existing.created_at.isoformat(),
                'expires_at': existing.expires_at.isoformat(),
            }), 200
        
        # Create new share link
        share_link = SharedLink(review_id=review_id)
        db.session.add(share_link)
        db.session.commit()
        
        return jsonify({
            'token': share_link.token,
            'url': f'/share/{share_link.token}',
            'created_at': share_link.created_at.isoformat(),
            'expires_at': share_link.expires_at.isoformat(),
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/shared/<token>', methods=['GET'])
def get_shared_review(token):
    """Get a review via share token"""
    try:
        share_link = SharedLink.query.filter_by(token=token).first()
        
        if not share_link:
            return jsonify({'error': 'Share link not found'}), 404
        
        if share_link.is_expired():
            return jsonify({'error': 'Share link expired'}), 410
        
        review = share_link.review
        return jsonify({
            'id': review.id,
            'filename': review.filename,
            'language': review.language,
            'code_content': review.code_content,
            'quality_score': review.quality_score,
            'bug_count': review.bug_count,
            'security_count': review.security_count,
            'suggestion_count': review.suggestion_count,
            'security_score': review.security_score,
            'reliability_score': review.reliability_score,
            'maintainability_score': review.maintainability_score,
            'complexity_score': review.complexity_score,
            'analysis_duration': review.analysis_duration,
            'created_at': review.created_at.isoformat(),
            'issues': [issue.to_dict() for issue in review.issues],
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ═══════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'Code file too large (max 5MB)'}), 413


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
