from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
import datetime

def generate_receipt_pdf(payment):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        alignment=TA_LEFT,
        textColor=colors.darkblue
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=6,
        alignment=TA_LEFT
    )
    
    # Title
    elements.append(Paragraph("COLLEGE FEE PAYMENT RECEIPT", title_style))
    elements.append(Spacer(1, 20))
    
    # Receipt details
    receipt_data = [
        ['Receipt Number:', payment.receipt_number or 'N/A'],
        ['Date:', payment.transaction_date.strftime('%d/%m/%Y %I:%M %p')],
        ['Payment ID:', payment.razorpay_payment_id or 'N/A'],
        ['Status:', payment.get_status_display()],
    ]
    
    receipt_table = Table(receipt_data, colWidths=[2*inch, 3*inch])
    receipt_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(receipt_table)
    elements.append(Spacer(1, 20))
    
    # Student details
    elements.append(Paragraph("STUDENT DETAILS", header_style))
    
    student_data = [
        ['College ID:', payment.student.college_id],
        ['Name:', payment.student.full_name],
        ['Email:', payment.student.email],
        ['Phone:', payment.student.phone_number],
        ['Admission Type:', payment.student.get_admission_type_display()],
    ]
    
    student_table = Table(student_data, colWidths=[2*inch, 3*inch])
    student_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(student_table)
    elements.append(Spacer(1, 20))
    
    # Payment details
    elements.append(Paragraph("PAYMENT DETAILS", header_style))
    
    payment_data = [
        ['Fee Type:', payment.get_fee_type_display()],
        ['Amount Paid:', f"₹{payment.amount}"],
        ['Payment Method:', 'Online (Razorpay)'],
        ['Transaction ID:', payment.razorpay_payment_id or 'N/A'],
    ]
    
    payment_table = Table(payment_data, colWidths=[2*inch, 3*inch])
    payment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(payment_table)
    elements.append(Spacer(1, 30))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    
    elements.append(Paragraph("This is a computer-generated receipt and does not require a signature.", footer_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("For any queries, please contact the college administration.", footer_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer