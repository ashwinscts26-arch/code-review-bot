from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from io import BytesIO
import csv
from datetime import datetime


class ExportService:
    """Handles exporting reviews to various formats"""
    
    @staticmethod
    def export_to_pdf(review) -> BytesIO:
        """Export review to PDF"""
        buffer = BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
        )
        
        # Container for elements
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
        ))
        
        styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold',
        ))
        
        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['BodyText'],
            fontSize=10,
            leading=14,
        ))
        
        # Title
        elements.append(Paragraph('Code Review Report', styles['CustomTitle']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Summary Section
        summary_data = [
            ['Filename:', review.filename],
            ['Language:', review.language],
            ['Date:', review.created_at.strftime('%Y-%m-%d %H:%M:%S')],
            ['Quality Score:', f"{review.quality_score}/100"],
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e2e8f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Metrics Section
        elements.append(Paragraph('Quality Metrics', styles['CustomHeading2']))
        
        metrics_data = [
            ['Security Score:', f"{review.security_score}/100"],
            ['Reliability Score:', f"{review.reliability_score}/100"],
            ['Maintainability Score:', f"{review.maintainability_score}/100"],
            ['Complexity Score:', f"{review.complexity_score}/100"],
        ]
        
        metrics_table = Table(metrics_data, colWidths=[2*inch, 4*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f1f5f9')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Issues Summary
        elements.append(Paragraph('Issues Summary', styles['CustomHeading2']))
        
        issue_summary = f"""
        <b>Total Issues:</b> {len(review.issues)}<br/>
        <b>Critical:</b> {len([i for i in review.issues if i.severity == 'critical'])}<br/>
        <b>High:</b> {len([i for i in review.issues if i.severity == 'high'])}<br/>
        <b>Medium:</b> {len([i for i in review.issues if i.severity == 'medium'])}<br/>
        <b>Low:</b> {len([i for i in review.issues if i.severity == 'low'])}
        """
        elements.append(Paragraph(issue_summary, styles['CustomBody']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Issues Detail
        if review.issues:
            elements.append(Paragraph('Detailed Issues', styles['CustomHeading2']))
            
            for issue in review.issues[:20]:  # Limit to first 20 issues
                issue_text = f"""
                <b>Line {issue.line_number}: {issue.title}</b><br/>
                <b>Category:</b> {issue.category} | <b>Severity:</b> {issue.severity.upper()}<br/>
                <b>Description:</b> {issue.description}<br/>
                """
                
                if issue.suggested_fix:
                    issue_text += f"<b>Fix:</b> {issue.suggested_fix}<br/>"
                
                elements.append(Paragraph(issue_text, styles['CustomBody']))
                elements.append(Spacer(1, 0.1*inch))
            
            if len(review.issues) > 20:
                elements.append(Paragraph(
                    f'... and {len(review.issues) - 20} more issues',
                    styles['CustomBody']
                ))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer_text = f"<i>Generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</i>"
        elements.append(Paragraph(footer_text, styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return buffer
    
    @staticmethod
    def export_to_csv(review) -> str:
        """Export issues to CSV"""
        output = []
        
        # Header
        output.append([
            'Line Number',
            'Severity',
            'Category',
            'Type',
            'Title',
            'Description',
            'Suggested Fix',
            'CWE',
        ])
        
        # Issues
        for issue in review.issues:
            output.append([
                str(issue.line_number),
                issue.severity,
                issue.category,
                issue.type,
                issue.title,
                issue.description,
                issue.suggested_fix or '',
                issue.cwe or '',
            ])
        
        # Convert to CSV string
        csv_buffer = BytesIO()
        writer = csv.writer(csv_buffer)
        writer.writerows(output)
        
        return csv_buffer.getvalue().decode('utf-8')
