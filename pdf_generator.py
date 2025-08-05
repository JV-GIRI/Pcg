from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os
import io
import base64
from typing import Dict, List
import matplotlib.pyplot as plt
import numpy as np

class MedicalReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for medical reports"""
        
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=TA_CENTER
        )
        
        # Header style
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkred,
            borderWidth=1,
            borderColor=colors.darkred,
            borderPadding=5
        )
        
        # Subheader style
        self.subheader_style = ParagraphStyle(
            'CustomSubHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            textColor=colors.darkblue
        )
        
        # Body style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6
        )
        
        # Footer style
        self.footer_style = ParagraphStyle(
            'CustomFooter',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
    
    def generate_report(self, patient_data: Dict, diagnosis_data: Dict, output_path: str) -> str:
        """Generate complete medical report PDF"""
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        story = []
        
        # Header
        story.extend(self._create_header())
        
        # Patient Information
        story.extend(self._create_patient_section(patient_data))
        
        # Diagnosis Results
        story.extend(self._create_diagnosis_section(diagnosis_data))
        
        # Technical Analysis
        story.extend(self._create_technical_section(diagnosis_data))
        
        # Recommendations
        story.extend(self._create_recommendations_section(diagnosis_data))
        
        # Footer
        story.extend(self._create_footer())
        
        doc.build(story)
        return output_path
    
    def _create_header(self) -> List:
        """Create report header"""
        elements = []
        
        # Title
        elements.append(Paragraph("HEARTEST", self.title_style))
        elements.append(Paragraph("Giri's AI PCG Analyzer", self.body_style))
        elements.append(Paragraph("Valvular Heart Disease Diagnostic Report", self.subheader_style))
        elements.append(Spacer(1, 20))
        
        # Date and time
        now = datetime.now()
        date_str = now.strftime("%B %d, %Y at %I:%M %p")
        elements.append(Paragraph(f"Report Generated: {date_str}", self.body_style))
        elements.append(Spacer(1, 30))
        
        return elements
    
    def _create_patient_section(self, patient_data: Dict) -> List:
        """Create patient information section"""
        elements = []
        
        elements.append(Paragraph("PATIENT INFORMATION", self.header_style))
        
        # Patient details table
        patient_table_data = [
            ["Name:", patient_data.get('name', 'N/A')],
            ["Age:", f"{patient_data.get('age', 'N/A')} years"],
            ["Gender:", patient_data.get('gender', 'N/A')],
            ["Height:", f"{patient_data.get('height', 'N/A')} cm"],
            ["Weight:", f"{patient_data.get('weight', 'N/A')} kg"],
            ["BMI:", f"{patient_data.get('bmi', 'N/A')} kg/m²"],
            ["Phone:", patient_data.get('phone', 'N/A')],
        ]
        
        patient_table = Table(patient_table_data, colWidths=[2*inch, 4*inch])
        patient_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.lightgrey]),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(patient_table)
        elements.append(Spacer(1, 20))
        
        # Clinical notes
        if patient_data.get('clinical_notes'):
            elements.append(Paragraph("Clinical Notes:", self.subheader_style))
            elements.append(Paragraph(patient_data['clinical_notes'], self.body_style))
            elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_diagnosis_section(self, diagnosis_data: Dict) -> List:
        """Create diagnosis results section"""
        elements = []
        
        elements.append(Paragraph("DIAGNOSTIC RESULTS", self.header_style))
        
        # Valve site and diagnosis
        valve_info = [
            ["Valve Site:", diagnosis_data.get('valve_name', 'N/A')],
            ["Primary Diagnosis:", diagnosis_data.get('primary_diagnosis', 'N/A')],
            ["Confidence Level:", f"{diagnosis_data.get('confidence_level', 'N/A')}%"],
            ["Severity:", diagnosis_data.get('severity', 'N/A')],
        ]
        
        diagnosis_table = Table(valve_info, colWidths=[2*inch, 4*inch])
        diagnosis_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.lightblue, colors.white]),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(diagnosis_table)
        elements.append(Spacer(1, 20))
        
        # Clinical findings
        if diagnosis_data.get('findings'):
            elements.append(Paragraph("Clinical Findings:", self.subheader_style))
            for finding in diagnosis_data['findings']:
                elements.append(Paragraph(f"• {finding}", self.body_style))
            elements.append(Spacer(1, 15))
        
        return elements
    
    def _create_technical_section(self, diagnosis_data: Dict) -> List:
        """Create technical analysis section"""
        elements = []
        
        elements.append(Paragraph("TECHNICAL ANALYSIS", self.header_style))
        
        # Analysis timestamp
        if diagnosis_data.get('analysis_timestamp'):
            timestamp = diagnosis_data['analysis_timestamp']
            elements.append(Paragraph(f"Analysis performed: {timestamp}", self.body_style))
            elements.append(Spacer(1, 10))
        
        # AI analysis details
        if diagnosis_data.get('simulation_mode'):
            elements.append(Paragraph("Analysis Mode: Simulation (Gemini AI not available)", self.body_style))
        else:
            elements.append(Paragraph("Analysis Mode: Gemini 2.5 Pro AI", self.body_style))
        
        elements.append(Spacer(1, 15))
        
        # Raw AI response (if available)
        if diagnosis_data.get('raw_response') and not diagnosis_data.get('simulation_mode'):
            elements.append(Paragraph("AI Analysis Report:", self.subheader_style))
            # Truncate if too long
            response = diagnosis_data['raw_response']
            if len(response) > 1000:
                response = response[:1000] + "..."
            elements.append(Paragraph(response, self.body_style))
            elements.append(Spacer(1, 15))
        
        return elements
    
    def _create_recommendations_section(self, diagnosis_data: Dict) -> List:
        """Create recommendations section"""
        elements = []
        
        elements.append(Paragraph("RECOMMENDATIONS", self.header_style))
        
        # Clinical recommendations
        if diagnosis_data.get('recommendations'):
            elements.append(Paragraph("Clinical Recommendations:", self.subheader_style))
            for rec in diagnosis_data['recommendations']:
                elements.append(Paragraph(f"• {rec}", self.body_style))
            elements.append(Spacer(1, 10))
        
        # Follow-up
        if diagnosis_data.get('follow_up'):
            elements.append(Paragraph("Follow-up:", self.subheader_style))
            elements.append(Paragraph(diagnosis_data['follow_up'], self.body_style))
            elements.append(Spacer(1, 15))
        
        # Disclaimer
        disclaimer = """
        <b>IMPORTANT DISCLAIMER:</b><br/>
        This AI-generated report is for educational and research purposes only. 
        It should not be used as a substitute for professional medical diagnosis or treatment. 
        Always consult with a qualified healthcare provider for proper medical evaluation and care.
        """
        elements.append(Paragraph(disclaimer, self.body_style))
        
        return elements
    
    def _create_footer(self) -> List:
        """Create report footer"""
        elements = []
        
        elements.append(Spacer(1, 30))
        elements.append(Paragraph("Generated by HEARTEST - Giri's AI PCG Analyzer", self.footer_style))
        elements.append(Paragraph("Advanced AI-powered phonocardiography analysis system", self.footer_style))
        
        return elements
    
    def create_multi_valve_report(self, patient_data: Dict, all_diagnoses: List[Dict], output_path: str) -> str:
        """Create comprehensive report for multiple valve sites"""
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        story = []
        
        # Header
        story.extend(self._create_header())
        
        # Patient Information
        story.extend(self._create_patient_section(patient_data))
        
        # Summary table
        story.append(Paragraph("COMPREHENSIVE VALVE ASSESSMENT", self.header_style))
        
        summary_data = [["Valve Site", "Diagnosis", "Severity", "Confidence"]]
        for diagnosis in all_diagnoses:
            summary_data.append([
                diagnosis.get('valve_name', 'N/A'),
                diagnosis.get('primary_diagnosis', 'N/A'),
                diagnosis.get('severity', 'N/A'),
                f"{diagnosis.get('confidence_level', 'N/A')}%"
            ])
        
        summary_table = Table(summary_data, colWidths=[1.5*inch, 2*inch, 1*inch, 1*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.white]),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 30))
        
        # Individual valve reports
        for i, diagnosis in enumerate(all_diagnoses):
            if i > 0:
                story.append(PageBreak())
            
            story.append(Paragraph(f"DETAILED ANALYSIS - {diagnosis.get('valve_name', 'Unknown')}", self.header_style))
            story.extend(self._create_diagnosis_section(diagnosis))
            story.extend(self._create_technical_section(diagnosis))
            story.extend(self._create_recommendations_section(diagnosis))
        
        # Footer
        story.extend(self._create_footer())
        
        doc.build(story)
        return output_path

# Global PDF generator instance
pdf_generator = MedicalReportGenerator()