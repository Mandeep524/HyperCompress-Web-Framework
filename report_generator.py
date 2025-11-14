"""
PDF Report Generator for Compression Analysis
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io


class CompressionReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()
    
    def _add_custom_styles(self):
        """Add custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=12,
            spaceBefore=12
        ))
    
    def generate_single_compression_report(self, compression_data):
        """Generate PDF report for a single compression operation"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        
        # Title
        title = Paragraph("Compression Analysis Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        story.append(Paragraph(f"<b>Generated:</b> {timestamp}", self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # File Information
        story.append(Paragraph("File Information", self.styles['SectionHeader']))
        file_info_data = [
            ['Property', 'Value'],
            ['File Name', compression_data.get('filename', 'N/A')],
            ['File Type', compression_data.get('file_type', 'N/A')],
            ['Algorithm', compression_data.get('algorithm', 'N/A')],
        ]
        
        file_info_table = Table(file_info_data, colWidths=[2*inch, 4*inch])
        file_info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(file_info_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Compression Metrics
        story.append(Paragraph("Compression Metrics", self.styles['SectionHeader']))
        metrics_data = [
            ['Metric', 'Value'],
            ['Original Size', f"{compression_data.get('original_size', 0)} bytes"],
            ['Compressed Size', f"{compression_data.get('compressed_size', 0)} bytes"],
            ['Compression Ratio', f"{compression_data.get('compression_ratio', 0):.4f}"],
            ['Space Savings', f"{compression_data.get('space_savings', 0):.2f}%"],
            ['Compression Time', f"{compression_data.get('compression_time', 0):.6f} seconds"],
            ['Decompression Time', f"{compression_data.get('decompression_time', 0):.6f} seconds"],
            ['Data Integrity', '✓ Verified' if compression_data.get('is_correct') else '✗ Failed'],
        ]
        
        metrics_table = Table(metrics_data, colWidths=[2.5*inch, 3.5*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        story.append(metrics_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Performance Analysis
        story.append(Paragraph("Performance Analysis", self.styles['SectionHeader']))
        
        ratio = compression_data.get('compression_ratio', 1)
        savings = compression_data.get('space_savings', 0)
        
        if ratio < 0.5:
            performance = "Excellent compression achieved"
        elif ratio < 0.7:
            performance = "Good compression performance"
        elif ratio < 0.9:
            performance = "Moderate compression"
        else:
            performance = "Limited compression (data may not be suitable for this algorithm)"
        
        story.append(Paragraph(f"<b>Overall Performance:</b> {performance}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Space Saved:</b> {savings:.2f}% of original size", self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def generate_comparison_report(self, comparison_results):
        """Generate PDF report comparing multiple algorithms"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        
        # Title
        title = Paragraph("Algorithm Comparison Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        story.append(Paragraph(f"<b>Generated:</b> {timestamp}", self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Summary
        story.append(Paragraph("Comparison Summary", self.styles['SectionHeader']))
        story.append(Paragraph(f"Total algorithms tested: {len(comparison_results)}", self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Comparison Table
        story.append(Paragraph("Detailed Comparison", self.styles['SectionHeader']))
        
        comparison_data = [['Algorithm', 'Ratio', 'Savings %', 'Comp. Time', 'Decomp. Time', 'Status']]
        
        for result in comparison_results:
            if not result.get('error'):
                comparison_data.append([
                    result.get('algorithm', 'N/A'),
                    f"{result.get('compression_ratio', 0):.4f}",
                    f"{result.get('space_savings', 0):.2f}%",
                    f"{result.get('compression_time', 0):.6f}s",
                    f"{result.get('decompression_time', 0):.6f}s",
                    '✓' if result.get('is_correct') else '✗'
                ])
        
        comparison_table = Table(comparison_data, colWidths=[1.2*inch, 1*inch, 1*inch, 1.2*inch, 1.2*inch, 0.8*inch])
        comparison_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        story.append(comparison_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Best Performers
        story.append(Paragraph("Best Performers", self.styles['SectionHeader']))
        
        valid_results = [r for r in comparison_results if not r.get('error')]
        if valid_results:
            best_ratio = min(valid_results, key=lambda x: x.get('compression_ratio', 1))
            fastest = min(valid_results, key=lambda x: x.get('compression_time', 999))
            
            story.append(Paragraph(f"🏆 <b>Best Compression Ratio:</b> {best_ratio.get('algorithm')} ({best_ratio.get('compression_ratio'):.4f})", self.styles['Normal']))
            story.append(Paragraph(f"⚡ <b>Fastest Compression:</b> {fastest.get('algorithm')} ({fastest.get('compression_time'):.6f}s)", self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def generate_history_report(self, history_data, statistics):
        """Generate PDF report for compression history"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        
        # Title
        title = Paragraph("Compression History Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        story.append(Paragraph(f"<b>Generated:</b> {timestamp}", self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Statistics
        story.append(Paragraph("Overall Statistics", self.styles['SectionHeader']))
        story.append(Paragraph(f"<b>Total Compressions:</b> {statistics.get('total_compressions', 0)}", self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        # Algorithm breakdown
        algo_stats = statistics.get('algorithm_stats', {})
        story.append(Paragraph("<b>By Algorithm:</b>", self.styles['Normal']))
        for algo, count in algo_stats.items():
            story.append(Paragraph(f"  • {algo}: {count}", self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        # File type breakdown
        file_stats = statistics.get('file_type_stats', {})
        story.append(Paragraph("<b>By File Type:</b>", self.styles['Normal']))
        for ftype, count in file_stats.items():
            story.append(Paragraph(f"  • {ftype}: {count}", self.styles['Normal']))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Recent History (limited to first 20)
        story.append(Paragraph("Recent Compression History", self.styles['SectionHeader']))
        
        history_table_data = [['Date', 'File Type', 'Algorithm', 'Ratio', 'Savings %']]
        
        for record in history_data[:20]:
            date_str = record.get('timestamp', datetime.now()).strftime("%Y-%m-%d %H:%M") if isinstance(record.get('timestamp'), datetime) else 'N/A'
            history_table_data.append([
                date_str,
                record.get('file_type', 'N/A'),
                record.get('algorithm', 'N/A'),
                f"{record.get('compression_ratio', 0):.4f}",
                f"{record.get('space_savings', 0):.2f}%"
            ])
        
        history_table = Table(history_table_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1*inch, 1*inch])
        history_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        story.append(history_table)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer


# Singleton instance
_report_generator = None

def get_report_generator():
    """Get or create report generator instance"""
    global _report_generator
    if _report_generator is None:
        _report_generator = CompressionReportGenerator()
    return _report_generator
