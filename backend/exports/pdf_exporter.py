from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime


class PDFExporter:
    """Exports code reviews as professional PDF reports"""
    
    def __init__(self, review):
        self.review = review
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=30,
            alignment=TA_CENTER,
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHead',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=12,
            spaceBefore=12,
        ))
    
    def generate(self) -> bytes:
        """Generate PDF report"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        
        # Title
        story.append(Paragraph('Code Review Report', self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2 * inch))
        
        # Header info
        header_data = [
            ['Filename:', self.review.filename],
            ['Language:', self.review.language],
            ['Analysis Date:', self.review.created_at.strftime('%Y-%m-%d %H:%M:%S')],
            ['Analysis Duration:', f'{self.review.analysis_duration}s'],
        ]
        
        header_table = Table(header_data, colWidths=[2 * inch, 4 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e2e8f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Quality Scores
        story.append(Paragraph('Quality Scores', self.styles['SectionHead']))
        scores_data = [
            ['Metric', 'Score'],
            ['Overall Quality', f'{self.review.quality_score}/100'],
            ['Security', f'{self.review.security_score}/100'],
            ['Reliability', f'{self.review.reliability_score}/100'],
            ['Maintainability', f'{self.review.maintainability_score}/100'],
            ['Complexity', f'{self.review.complexity_score}/100'],
        ]
        
        scores_table = Table(scores_data, colWidths=[3 * inch, 3 * inch])
        scores_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f9ff')]),
        ]))
        story.append(scores_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Issues Summary
        story.append(Paragraph('Issues Summary', self.styles['SectionHead']))
        summary_data = [
            ['Category', 'Count'],
            ['Bugs', str(self.review.bug_count)],
            ['Security Issues', str(self.review.security_count)],
            ['Code Quality Issues', str(self.review.suggestion_count)],
        ]
        
        summary_table = Table(summary_data, colWidths=[3 * inch, 3 * inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ef4444')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fef2f2')]),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Issues Detail
        if self.review.issues:
            story.append(PageBreak())
            story.append(Paragraph('Detailed Issues', self.styles['SectionHead']))
            
            for issue in self.review.issues:
                severity_color = self._get_severity_color(issue.severity)
                
                issue_header = Paragraph(
                    f'<b>[{issue.severity.upper()}]</b> Line {issue.line_number}: {issue.title}',
                    self.styles['Heading3']
                )
                story.append(issue_header)
                
                # Issue details table
                issue_details = [
                    ['Type:', issue.type],
                    ['Category:', issue.category],
                    ['Description:', issue.description],
                ]
                
                if issue.explanation:
                    issue_details.append(['Explanation:', issue.explanation])
                if issue.impact:
                    issue_details.append(['Impact:', issue.impact])
                if issue.suggested_fix:
                    issue_details.append(['Suggested Fix:', issue.suggested_fix])
                if issue.cwe:
                    issue_details.append(['CWE:', issue.cwe])
                
                issue_table = Table(issue_details, colWidths=[1.5 * inch, 5 * inch])
                issue_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e2e8f0')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ]))
                story.append(issue_table)
                story.append(Spacer(1, 0.2 * inch))
        
        # Footer
        story.append(Spacer(1, 0.5 * inch))
        footer = Paragraph(
            '<i>This report was generated by Code Review Bot. For educational and development purposes only.</i>',
            self.styles['Normal']
        )
        story.append(footer)
        
        # Build PDF
        doc.build(story)
        return buffer.getvalue()
    
    def _get_severity_color(self, severity: str) -> str:
        """Get color for severity level"""
        colors_map = {
            'critical': '#dc2626',
            'high': '#ea580c',
            'medium': '#f59e0b',
            'low': '#eab308',
            'info': '#06b6d4',
        }
        return colors_map.get(severity, '#gray')
