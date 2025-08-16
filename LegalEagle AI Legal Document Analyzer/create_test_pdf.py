#!/usr/bin/env python3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_test_contract_pdf():
    filename = "test_contract.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "SERVICE AGREEMENT")
    
    # Content
    c.setFont("Helvetica", 12)
    y_position = height - 100
    
    contract_text = [
        'This Service Agreement ("Agreement") is entered into on January 1, 2024, between',
        'ABC Company ("Provider"), a Delaware corporation located at 123 Business Street,',
        'New York, NY 10001, and XYZ Corp ("Client"), a California LLC located at',
        '456 Client Avenue, Los Angeles, CA 90210.',
        '',
        '1. SERVICES',
        'Provider shall provide software development services as outlined in Exhibit A.',
        '',
        '2. PAYMENT TERMS',
        'Client shall pay Provider $50,000 within 30 days of invoice. Late payments',
        'subject to 2% monthly interest.',
        '',
        '3. TERM AND TERMINATION',
        'This Agreement shall commence on January 1, 2024 and continue for 12 months.',
        'Either party may terminate with 30 days written notice. This Agreement shall',
        'automatically renew for successive 12-month periods unless either party',
        'provides 60 days written notice.',
        '',
        '4. LIABILITY',
        'PROVIDER\'S LIABILITY SHALL BE UNLIMITED. Client shall indemnify Provider',
        'against all claims.',
        '',
        '5. CONFIDENTIALITY',
        'Client agrees not to disclose any confidential information for a period of',
        '5 years after termination.',
        '',
        '6. NON-COMPETE',
        'Client agrees not to compete with Provider anywhere in North America for',
        '3 years after termination.',
        '',
        '7. GOVERNING LAW',
        'This Agreement shall be governed by the laws of Delaware. Any disputes shall',
        'be resolved through binding arbitration with waiver of jury trial.',
        '',
        '8. INTELLECTUAL PROPERTY',
        'All work product created under this Agreement shall become the exclusive',
        'property of Provider.',
        '',
        'IN WITNESS WHEREOF, the parties have executed this Agreement.',
        '',
        'ABC Company                    XYZ Corp',
        'By: _________________         By: _________________'
    ]
    
    for line in contract_text:
        c.drawString(50, y_position, line)
        y_position -= 15
        if y_position < 50:  # Start new page if needed
            c.showPage()
            y_position = height - 50
            c.setFont("Helvetica", 12)
    
    c.save()
    print(f"Created {filename}")

if __name__ == "__main__":
    create_test_contract_pdf()