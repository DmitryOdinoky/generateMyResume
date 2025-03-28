import markdown
import pdfkit
import os
import argparse

def generate_resume_pdf(markdown_file='README.md', output_file='resume.pdf', css_file=None):
    """
    Generate a PDF resume from a Markdown file using pdfkit
    
    Args:
        markdown_file (str): Path to the markdown file
        output_file (str): Path for the output PDF file
        css_file (str, optional): Path to custom CSS file
    """
    # Check if the markdown file exists
    if not os.path.exists(markdown_file):
        print(f"Error: {markdown_file} does not exist!")
        return
    
    # Read the markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['tables', 'attr_list'])
    
    # Add basic styling
    default_css = """
    body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
        margin: 2cm;
        color: #333;
    }
    h1 { color: #2c3e50; font-size: 28px; }
    h2 { color: #3498db; font-size: 20px; border-bottom: 1px solid #eee; }
    h3 { color: #2c3e50; font-size: 16px; }
    a { color: #3498db; }
    img { max-width: 150px; border-radius: 50%; }
    """
    
    # Create HTML with proper head section
    html_document = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Resume</title>
        <style>{default_css}</style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Create temporary HTML file
    temp_html = 'temp_resume.html'
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html_document)
    
    # Convert to PDF
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': 'UTF-8',
        'enable-local-file-access': None,  # Enable access to local files
    }
    
    # Add CSS file if provided
    if css_file and os.path.exists(css_file):
        options['user-style-sheet'] = css_file
    
    # Path to wkhtmltopdf executable - CHANGE THIS TO YOUR ACTUAL PATH
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    
    try:
        # Use configuration to specify wkhtmltopdf location
        pdfkit.from_file(temp_html, output_file, options=options, configuration=config)
        print(f"PDF resume generated successfully: {output_file}")
    except Exception as e:
        print(f"Error generating PDF: {e}")
        print("If wkhtmltopdf is installed but not being found, check the path in this script")
        print("You need to modify the path in the line: config = pdfkit.configuration(wkhtmltopdf='...')")
        print("Common paths are:")
        print("  - C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
        print("  - C:/Program Files (x86)/wkhtmltopdf/bin/wkhtmltopdf.exe")
    
    # Clean up temporary file
    if os.path.exists(temp_html):
        os.remove(temp_html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert Markdown resume to PDF')
    parser.add_argument('--input', '-i', default='README.md', help='Input markdown file path')
    parser.add_argument('--output', '-o', default='resume.pdf', help='Output PDF file path')
    parser.add_argument('--css', '-c', help='Custom CSS file path')
    
    args = parser.parse_args()
    
    generate_resume_pdf(args.input, args.output, args.css)