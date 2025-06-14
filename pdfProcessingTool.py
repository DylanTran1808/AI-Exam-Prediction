import requests
import json
from dotenv import load_dotenv
import pdfplumber
import os
import csv
import io

load_dotenv()

api_key = os.getenv("API_KEY")
api_url = os.getenv("API_URL")

def extract_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def create_request(pdf_path):
    return requests.post(
        url = api_url,
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        data = json.dumps({
            "model": "deepseek/deepseek-r1-0528:free",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a highly accurate and organized data extraction assistant specialized in analyzing academic exam text and converting it into structured, labeled CSV data for educational datasets. You will receive raw text extracted from university-level exams. Your goal is to extract structured information from this text and convert it into a CSV format with the following columns: 1. ExamID: A unique identifier for the exam, formatted as Exam_[Year] or Resit_[Year] (e.g., Exam_2025, Resit_2023). 2. QuestionID: A unique identifier for each question, formatted as [E if is Exam/ R if is Resit + 2 last number of the year]_Q[Number, if question has subquestions mark them in alphabetical order] (e.g., E_25_Q1, R_23_Q2a). 3. Year:  Determine the year the exam was conducted. 4. Topic: A short label summarizing the academic topic or subtopic (e.g., Microservices Architecture, Test-Driven Development). 5. Difficulty: A difficulty rating inferred from the question's complexity (Easy, Medium, Hard). Use Hard for open-ended or multi-part questions, Medium for applied concepts, and Easy for definitions or simple matches. 6 AnswerType: Either Multiple Choice or Written (use Written for fill-in, open-ended, or diagram-based questions).Rules for Consistency: ExamID: Derive from explicit year mentions (e.g., Exam 2025 → Exam_2025). If absent, infer from context (e.g., 2023_Exam → Exam_2023). Default to NG if unclear. QuestionID: Always prefix with the ExamID (e.g., E_25_Q1). Topic: Use standardized terms (e.g., SOLID Principles, Git Commands). Difficulty: Default to Medium if uncertain.AnswerType: Classify Multiple Choice only for explicit A/B/C options; otherwise, use Written. Output Format: Strict CSV with columns in order: ExamID, QuestionID, Year, Topic, Difficulty, AnswerType. No explanations or extra text.",
                },
                {
                    "role": "user",
                    "content": extract_text(pdf_path)
                }
            ]
        })
    )
    
def process_pdf(pdf_path):
    response = create_request(pdf_path)
    if response.status_code == 200:
        result = response.json()
        try:
            csv_text = result["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise Exception(f"Unexpected response format: {e}\nResponse: {result}")

        # Parse CSV text into headers and rows
        csv_reader = csv.reader(io.StringIO(csv_text.strip()))
        rows = list(csv_reader)
        headers = rows[0]
        data_rows = rows[1:]

        return {
            "headers": headers,
            "rows": data_rows
        }
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")