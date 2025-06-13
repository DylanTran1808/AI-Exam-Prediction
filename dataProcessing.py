import openai
import requests
import json

import pdfplumber

def extract_text_pdfplumber(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])




print(extract_text_pdfplumber("data/Calculus - Data/Exam2013_calculus.pdf"))