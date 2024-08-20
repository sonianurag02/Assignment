import fitz  # PyMuPDF
import json
import re

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    document = fitz.open(pdf_path)
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

# Parse the extracted text
def extract_info(text):
    data = {}
    sections = re.split(r'\n(?=\S)', text)
    for section in sections:
        if 'Plumbing Services' in section:
            continue
        category = section.split('\n')[0]
        details = re.split(r'(?=\●)', section)
        data[category] = {}
        for detail in details[1:]:
            title, content = detail.split(':', 1)
            content = content.strip()
            if title == 'Minor Fixes':
                data[category]['Minor Fixes'] = content.split('\n')
            elif title == 'Average Repair Cost':
                data[category]['Average Repair Cost'] = content
            elif title == 'Replacement Time':
                data[category]['Replacement Time'] = content
    return data

# Convert extracted data to JSONL
def convert_to_jsonl(data, output_file):
    with open(output_file, 'w') as f:
        for service, details in data.items():
            for key, value in details.items():
                if isinstance(value, list):
                    prompt = f"What are some minor fixes for {service}?"
                    completion = " ".join(value)
                    f.write(json.dumps({"prompt": prompt, "completion": completion}) + "\n")
                elif key == "Average Repair Cost":
                    prompt = f"What is the average repair cost for {service}?"
                    completion = value
                    f.write(json.dumps({"prompt": prompt, "completion": completion}) + "\n")
                elif key == "Replacement Time":
                    prompt = f"What is the replacement time for {service}?"
                    completion = value
                    f.write(json.dumps({"prompt": prompt, "completion": completion}) + "\n")

if __name__ == '__main__':
    pdf_text = extract_text_from_pdf('services.pdf')  # Replace with your PDF path
    data = extract_info(pdf_text)
    convert_to_jsonl(data, 'training_data.jsonl')
