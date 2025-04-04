import markdown
import os
import argparse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT

def generate_resume_pdf(markdown_file='README.md', output_file='resume.pdf'):
    """
    Generate a PDF resume from a Markdown file using a simple approach
    """
    # Check if the markdown file exists
    if not os.path.exists(markdown_file):
        print(f"Error: {markdown_file} does not exist!")
        return
    
    # Read the markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['tables'])
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=36,
        bottomMargin=36
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Add custom styles
    title_style = ParagraphStyle(
        name='Title',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        name='Heading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.blue
    )
    
    # Use the SAME color for all company names
    subheading_style = ParagraphStyle(
        name='Subheading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.blue  # Consistent blue color for all company names
    )
    
    normal_style = ParagraphStyle(
        name='Normal',
        parent=styles['Normal'],
        fontSize=10
    )
    
    # Style for position and years (bold)
    position_style = ParagraphStyle(
        name='Position',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica-Bold'  # Make position and years bold
    )
    
    contact_style = ParagraphStyle(
        name='Contact',
        parent=styles['Normal'],
        fontSize=10,
        leading=14  # More space between lines
    )
    
    # Build PDF elements
    elements = []
    
    # Add title
    elements.append(Paragraph("Dmitrijs Odinokijs", title_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Add subtitle
    elements.append(Paragraph("Engineer, Researcher, Developer", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Create contact info table with photo
    try:
        if os.path.exists("myphoto.png"):
            img = Image("myphoto.png", width=1.5*inch, height=1.5*inch)
        else:
            img = Paragraph("Photo not found", normal_style)
            
        contact_info = Paragraph(
            "LinkedIn: <a href='https://www.linkedin.com/in/dmitry-odinoky-bb90a937' color='blue'>https://www.linkedin.com/in/dmitry-odinoky-bb90a937</a><br/>"
            "GitHub: <a href='https://github.com/DmitryOdinoky' color='blue'>https://github.com/DmitryOdinoky</a><br/>"
            "Email: <a href='mailto:dmitry.odinoky@gmail.com' color='blue'>dmitry.odinoky@gmail.com</a><br/>"
            "Phone: +371 26708549<br/>"
            "Birth: November 18, 1986<br/>"
            "Citizenship: Latvian", 
            contact_style
        )
        
        # Create a table with contact info on left, photo on right
        data = [[contact_info, img]]
        table = Table(data, colWidths=[4*inch, 2*inch])
        
        # Add style to the table - thin border with rounded corners
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),  # Center the image
            ('LINEBELOW', (0, 0), (0, 0), 1, colors.white),  # Invisible border
            ('LINEABOVE', (0, 0), (0, 0), 1, colors.white),
            ('LINEBEFORE', (0, 0), (0, 0), 1, colors.white),
            ('LINEAFTER', (0, 0), (0, 0), 1, colors.white),
            ('LINEBELOW', (1, 0), (1, 0), 1, colors.white),
            ('LINEABOVE', (1, 0), (1, 0), 1, colors.white),
            ('LINEBEFORE', (1, 0), (1, 0), 1, colors.white),
            ('LINEAFTER', (1, 0), (1, 0), 1, colors.white),
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('ROUNDEDCORNERS', [10, 10, 10, 10]),
        ]))
        
        elements.append(table)
    except Exception as e:
        print(f"Error creating contact table: {e}")
        # Fallback to basic contact info if table fails
        elements.append(Paragraph("LinkedIn: <a href='https://www.linkedin.com/in/dmitry-odinoky-bb90a937' color='blue'>https://www.linkedin.com/in/dmitry-odinoky-bb90a937</a>", normal_style))
        elements.append(Paragraph("GitHub: <a href='https://github.com/DmitryOdinoky' color='blue'>https://github.com/DmitryOdinoky</a>", normal_style))
        elements.append(Paragraph("Email: <a href='mailto:dmitry.odinoky@gmail.com' color='blue'>dmitry.odinoky@gmail.com</a>", normal_style))
        elements.append(Paragraph("Phone: +371 26708549", normal_style))
        elements.append(Paragraph("Birth: November 18, 1986", normal_style))
        elements.append(Paragraph("Citizenship: Latvian", normal_style))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Add summary section
    elements.append(Paragraph("Summary", heading_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("MSc (Eng) focused on robotics, artificial intelligence, acoustics, and human perception. Researcher/engineer/developer with wide skillset and strong background in music/audio industry.", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Add work experience
    elements.append(Paragraph("Work Experience", heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # ShipProjects - with position and years in bold
    elements.append(Paragraph("<a href='https://shipprojects.net/' color='blue'>ShipProjects</a>", subheading_style))
    elements.append(Paragraph("<b>Data Scientist / ML Engineer</b> | <b>2024-08 - present</b>", position_style))
    elements.append(Paragraph("Developed a comprehensive pipeline for maritime vessel fuel consumption optimization. The system integrates ML models trained on historical voyage data, ship parameters, and real-time sensor readings of vessel performance and environmental conditions. Combined optimization algorithms with dynamic programming to generate actionable recommendations for captains, delivering visual feedback and specific engine power load suggestions for different voyage segments to maximize fuel efficiency.", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Sonarworks - with position and years in bold
    elements.append(Paragraph("<a href='https://www.sonarworks.com/' color='blue'>Sonarworks</a>", subheading_style))
    elements.append(Paragraph("<b>Research Engineer</b> | <b>2018-08 - 2024-08</b>", position_style))
    elements.append(Paragraph("Participated in the internal prototyping, development and testing of such products as SoundID Reference, VoiceAI and SoundID™ Audio Personalization App. Designed research tools using Matlab, Python, PostgreSQL, C#, and C++. Investigated research papers, created internal technical documentation. Organized data collection, ML model training and deployment.", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Yamaha - with position and years in bold
    elements.append(Paragraph("<a href='https://europe.yamaha.com/' color='blue'>Yamaha Music Europe</a>", subheading_style))
    elements.append(Paragraph("<b>Product Specialist, Customer Support</b> | <b>2012-09 - 2025-03</b>", position_style))
    elements.append(Paragraph("Work on part-time basis over 10 years, support product dealers by answering e-mail requests. Hosted public events for dealers and users, demonstrated hardware and software capabilities to musicians, music producers, and sound engineers.", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Dynamic Records - with position and years in bold
    elements.append(Paragraph("Dynamic Records", subheading_style))
    elements.append(Paragraph("<b>Ableton Certified Trainer, Steinberg Certified Trainer, Music Producer</b> | <b>2008-01 - 2018-04</b>", position_style))
    elements.append(Paragraph("Became the only Ableton & Steinberg certified tutor in Baltics. <a href='https://www.ableton.com/en/certified-training/dmitry-odinoky/' color='blue'>Ableton Certified Trainer Profile</a>", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # SIA Dinamic Records - with position and years in bold
    elements.append(Paragraph("SIA Dinamic Records (soundschool.lv)", subheading_style))
    elements.append(Paragraph("<b>Lead Teacher, Project Manager</b> | <b>2009-01 - 2018-04</b>", position_style))
    elements.append(Paragraph("Led music production school and recording studio in Riga over 10 years. Taught classes, developed curriculum, managed implementation, handled business operations, and led a team of 3 people.", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Radio PIK - with position and years in bold
    elements.append(Paragraph("Radio PIK", subheading_style))
    elements.append(Paragraph("<b>Sound Production</b> | <b>2007-10 - 2010-12</b>", position_style))
    elements.append(Paragraph("Worked as sound engineer at local radio station.", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Education
    elements.append(Paragraph("Education", heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Apply the same bold formatting to education entries
    elements.append(Paragraph("Riga Technical University", subheading_style))
    elements.append(Paragraph("<b>Master of Engineering</b> | <b>2020 - 2023-06</b>", position_style))
    elements.append(Paragraph("MEng, Robotics and Artificial Intelligence", normal_style))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("Riga Technical University", subheading_style))
    elements.append(Paragraph("<b>Bachelor's Degree</b> | <b>2017 - 2020-06</b>", position_style))
    elements.append(Paragraph("Bachelor's degree, Robotics and Artificial Intelligence", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Qualifications
    elements.append(Paragraph("Qualifications", heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    qualifications = [
        "Data Science", "Machine Learning", "Psychoacoustics", 
        "Research and Development", "Acoustics", "Sound Design",
        "CI/CD, git, automated test frameworks",
        "Python for backend development, feature prototyping, data processing and visualization",
        "Python ML frameworks (PyTorch, TensorFlow, scikit-learn, etc)",
        "C++", "C#", "MATLAB", "SQL", "Docker", "Linux"
    ]
    
    for qual in qualifications:
        elements.append(Paragraph(f"• {qual}", normal_style))
    
    elements.append(Spacer(1, 0.2*inch))
    
    # Languages
    elements.append(Paragraph("Languages", heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("• English: Advanced", normal_style))
    elements.append(Paragraph("• Latvian: Advanced", normal_style))
    elements.append(Paragraph("• Russian: Native", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Certifications
    elements.append(Paragraph("Certifications", heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph("• RTU Zelta Fonds (GPA: 3.24/4.0) - <a href='https://www.rtu.lv/writable/public_files/RTU_zelta_fonds_2022.2023.pdf' color='blue'>Riga Technical University Golden Fund 2022/2023, p.37</a>", normal_style))
    elements.append(Paragraph("• Ableton Certified Trainer", normal_style))
    elements.append(Paragraph("• Audio Signal Processing for Music Applications (Universitat Pompeu Fabra of Barcelona)", normal_style))
    
    # Build the PDF
    doc.build(elements)
    print(f"PDF resume generated successfully: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert Markdown resume to PDF')
    parser.add_argument('--input', '-i', default='README.md', help='Input markdown file path')
    parser.add_argument('--output', '-o', default='resume.pdf', help='Output PDF file path')
    
    args = parser.parse_args()
    
    generate_resume_pdf(args.input, args.output)