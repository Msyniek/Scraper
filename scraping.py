import os
import time
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter

def get_text_with_br(content_div):
    # Preserves line breaks where <br> is used, for <div id="txtcontent0">
    lines = []
    for elem in content_div.children:
        if getattr(elem, 'name', None) == 'br':
            lines.append('\n')
        else:
            text = ''
            if hasattr(elem, 'get_text'):
                text = elem.get_text(strip=True)
            else:
                text = str(elem).strip()
            if text:
                lines.append(text)
    return [line for line in ''.join(lines).split('\n') if line.strip()]

def extract_txtnav_content(content_div):
    # Extracts narrative text from <div class="txtnav">, handling <br> tags and &emsp;
    lines = []
    for elem in content_div.children:
        if getattr(elem, 'name', None) == 'br':
            lines.append('\n')
        elif getattr(elem, 'name', None) in ['h1', 'div', 'script']:
            # Skip headings, metadata, ads/scripts
            continue
        else:
            text = elem if isinstance(elem, str) else elem.get_text(separator='', strip=True)
            # Replace HTML entities and Unicode spaces
            text = text.replace('\xa0', ' ').replace('&emsp;', '    ')
            if text:
                lines.append(text)
    # Handle multiple consecutive <br> as blank lines
    return [line for line in ''.join(lines).split('\n') if line.strip()]

def choose_extraction_method():
    print("Choose extraction method:")
    print("1. Extract from <div id='txtcontent0'> (twkan)")
    print("2. Extract from <div class='txtnav'> (69)")
    choice = input("Enter 1 or 2: ").strip()
    return 'txtcontent0' if choice == '1' else 'txtnav'

current_url =  input("Enter the start URL: ").strip()

script_dir = os.path.dirname(os.path.abspath(__file__))

# PDF setup
pdf_file = os.path.join(script_dir, input("Enter the PDF file name (default: example.pdf): ").strip() or "example.pdf")
c = canvas.Canvas(pdf_file, pagesize=letter)
width, height = letter
y_position = height - 50

# Register font
font_path =  os.path.join(script_dir, "fonts\\NotoSerifCJKsc-VF.ttf") # https://github.com/notofonts/noto-cjk
print(f"Using font file: {font_path}")
print(f"Font exists: {os.path.exists(font_path)}")
print(f"Is the font readable? {os.access(font_path, os.R_OK)}")
pdfmetrics.registerFont(TTFont('NotoSerifCJKsc-VF', font_path))

extraction_method = choose_extraction_method()

timeDelay = int(input("Enter the time to delay between requests (Cloudflare)(default: 2): ").strip() or 2)

driver = uc.Chrome()

initial_delay = True

try:
    while current_url:
        driver.get(current_url)
        if initial_delay:
            time.sleep(10)  # Initial wait for Cloudflare/JS challenge
            initial_delay = False
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Extraction logic based on user's choice
        if extraction_method == 'txtcontent0':
            content = soup.find('div', id='txtcontent0')
            if content:
                lines = get_text_with_br(content)
            else:
                lines = []
        else:
            content = soup.find('div', class_='txtnav')
            if content:
                lines = extract_txtnav_content(content)
            else:
                lines = []

        # Write extracted lines to PDF
        if lines:
            c.setFont('NotoSerifCJKsc-VF', 12)
            for line in lines:
                print(line)
                # Manual wrapping for long lines
                max_char_per_line = 43
                for i in range(0, len(line), max_char_per_line):
                    c.drawString(50, y_position, line[i:i+max_char_per_line])
                    y_position -= 15
                    if y_position < 50:
                        c.showPage()
                        c.setFont('NotoSerifCJKsc-VF', 12)
                        y_position = height - 50

        # Next chapter navigation
        next_link = soup.find("a", string="下一章")
        if next_link and "href" in next_link.attrs:
            current_url = requests.compat.urljoin(current_url, next_link["href"])
            time.sleep(timeDelay)
        else:
            current_url = None
finally:
    try:
        c.save()
        time.sleep(0.1)
        driver.quit()
        print(f"Content saved to {pdf_file}")
    except Exception as e:
        print(f"Error quitting driver: {e}")
    finally:
        print("If the errors are undetected_chromedriver __init__.py, line 843, in __del__ AND undetected_chromedriver __init__.py, line 798, in quit AND the script works you can ignore them OR visit https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/955")