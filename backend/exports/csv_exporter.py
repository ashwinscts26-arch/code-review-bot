import csv
from io import StringIO, BytesIO


class CSVExporter:
    """Exports code review issues as CSV"""
    
    def __init__(self, review):
        self.review = review
    
    def generate(self) -> bytes:
        """Generate CSV export"""
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Review ID',
            'Filename',
            'Language',
            'Analysis Date',
        ])
        
        writer.writerow([
            self.review.id,
            self.review.filename,
            self.review.language,
            self.review.created_at.isoformat(),
        ])
        
        writer.writerow([])  # Blank line
        
        # Write scores
        writer.writerow(['Quality Scores'])
        writer.writerow(['Metric', 'Score'])
        writer.writerow(['Overall', self.review.quality_score])
        writer.writerow(['Security', self.review.security_score])
        writer.writerow(['Reliability', self.review.reliability_score])
        writer.writerow(['Maintainability', self.review.maintainability_score])
        writer.writerow(['Complexity', self.review.complexity_score])
        
        writer.writerow([])  # Blank line
        
        # Write issues
        writer.writerow(['Issues'])
        writer.writerow([
            'Line',
            'Type',
            'Severity',
            'Category',
            'Title',
            'Description',
            'Suggested Fix',
            'CWE',
        ])
        
        for issue in self.review.issues:
            writer.writerow([
                issue.line_number,
                issue.type,
                issue.severity,
                issue.category,
                issue.title,
                issue.description,
                issue.suggested_fix or '',
                issue.cwe or '',
            ])
        
        # Convert to bytes
        csv_string = output.getvalue()
        return csv_string.encode('utf-8')
