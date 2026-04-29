import pdfplumber
import re
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def clean_text(text):
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)

    # Remove common noise
    text = re.sub(r'Page \d+', '', text)
    text = re.sub(r'P\.T\.O\.?', '', text)
    text = re.sub(r'\(cid:\d+\)', '', text)

    return text.strip()

def extract_year_from_filename(filename):
    match = re.search(r'(\d{2,4})', filename)
    if match:
        y = match.group()
        return int("20" + y) if len(y) == 2 else int(y)


def segment_questions(text, year, paper_name):
    questions = []

    text = re.split(r'SECTION\s*[-A-Z]+', text, flags=re.IGNORECASE)[-1]

    # Split by Q.1, Q.2, etc.
    main_qs = re.split(r'Q\.\s*(\d+)', text)

    for i in range(1, len(main_qs), 2):
        q_num = main_qs[i]
        q_text = main_qs[i + 1].strip()
        q_text = q_text.replace("\n", " ")

        # Extract Roman subparts (i., ii., iii.)
        sub_parts = re.split(
            r'\(\s*(i{1,3}|iv|v|vi{0,3}|ix|x)\s*\)',
            q_text,
            flags=re.IGNORECASE
        )


        if len(sub_parts) > 1:
            for j in range(1, len(sub_parts), 2):
                sub_label = sub_parts[j]
                sub_text = sub_parts[j + 1]

                sub_text = re.sub(r'\([a-d]\)', '', sub_text)
                sub_text = re.sub(r'\(\d+\)', '', sub_text)
                sub_text = re.sub(r'\b\d{1,2}\s+\d{1,2}\s+\d{1,2}\b', '', sub_text)
                sub_text = sub_text.strip()

                questions.append({
                    "year": year,
                    "paper": paper_name,
                    "question_number": f"{q_num}({sub_label.lower()})",
                    "marks": None,
                    "text": sub_text
                })
        else:
            q_text = re.sub(r'\([a-d]\)', '', q_text)
            q_text = re.sub(r'\(\d+\)', '', q_text)
            q_text = q_text.strip()

            questions.append({
                "year": year,
                "paper": paper_name,
                "question_number": q_num,
                "marks": None,
                "text": q_text
            })

    return questions


def parse_pdf(pdf_path):
    filename = os.path.basename(pdf_path)
    paper_name = filename.replace(".pdf", "")
    year = extract_year_from_filename(filename)

    raw_text = extract_text_from_pdf(pdf_path)
    cleaned_text = clean_text(raw_text)

    questions = segment_questions(cleaned_text, year, paper_name)

    return questions

