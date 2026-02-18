import pypdf
import sys

def extract_text_from_pdf(pdf_path):
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error extracting text: {e}"

if __name__ == "__main__":
    pdf_path = r"c:\Users\LENOVO\portfolio\Black White Minimalist CV Resume.pdf"
    print(extract_text_from_pdf(pdf_path))
