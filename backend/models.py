from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import secrets

db = SQLAlchemy()


class Review(db.Model):
    """Represents a code review"""
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    code_content = db.Column(db.Text, nullable=False)
    
    # Scores and metrics
    quality_score = db.Column(db.Integer, default=0)
    bug_count = db.Column(db.Integer, default=0)
    security_count = db.Column(db.Integer, default=0)
    suggestion_count = db.Column(db.Integer, default=0)
    
    # Score breakdown
    security_score = db.Column(db.Integer, default=0)
    reliability_score = db.Column(db.Integer, default=0)
    maintainability_score = db.Column(db.Integer, default=0)
    complexity_score = db.Column(db.Integer, default=0)
    
    # Metadata
    analysis_duration = db.Column(db.Float, default=0)  # seconds
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    issues = db.relationship('Issue', backref='review', lazy=True, cascade='all, delete-orphan')
    shared_links = db.relationship('SharedLink', backref='review', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'language': self.language,
            'code_content': self.code_content,
            'quality_score': self.quality_score,
            'bug_count': self.bug_count,
            'security_count': self.security_count,
            'suggestion_count': self.suggestion_count,
            'security_score': self.security_score,
            'reliability_score': self.reliability_score,
            'maintainability_score': self.maintainability_score,
            'complexity_score': self.complexity_score,
            'analysis_duration': self.analysis_duration,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'issues': [issue.to_dict() for issue in self.issues],
        }


class Issue(db.Model):
    """Represents a single issue found during analysis"""
    __tablename__ = 'issues'

    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    
    # Issue details
    type = db.Column(db.String(50), nullable=False)  # bug, security, quality, suggestion
    severity = db.Column(db.String(20), nullable=False)  # critical, high, medium, low, info
    category = db.Column(db.String(100), nullable=False)  # e.g., "SQL Injection", "Undefined Variable"
    
    # Location
    line_number = db.Column(db.Integer, nullable=False)
    end_line_number = db.Column(db.Integer, nullable=True)
    
    # Content
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    impact = db.Column(db.Text, nullable=True)
    suggested_fix = db.Column(db.Text, nullable=True)
    
    # Security reference
    cwe = db.Column(db.String(50), nullable=True)  # e.g., CWE-89
    cwe_url = db.Column(db.String(255), nullable=True)
    
    # Code context
    code_context = db.Column(db.Text, nullable=True)  # Snippet of code around the issue
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'severity': self.severity,
            'category': self.category,
            'line_number': self.line_number,
            'end_line_number': self.end_line_number,
            'title': self.title,
            'description': self.description,
            'explanation': self.explanation,
            'impact': self.impact,
            'suggested_fix': self.suggested_fix,
            'cwe': self.cwe,
            'cwe_url': self.cwe_url,
            'code_context': self.code_context,
        }


class SharedLink(db.Model):
    """Represents a shareable read-only link to a review"""
    __tablename__ = 'shared_links'

    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    
    # Token for sharing
    token = db.Column(db.String(64), unique=True, nullable=False, default=lambda: secrets.token_urlsafe(32))
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=30))
    
    def is_expired(self):
        return datetime.utcnow() > self.expires_at
    
    def to_dict(self):
        return {
            'id': self.id,
            'token': self.token,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'is_expired': self.is_expired(),
        }
