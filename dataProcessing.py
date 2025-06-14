from pdfProcessingTool import process_pdf
import os
import csv
from pathlib import Path

base_dir = Path("data")
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)
def process_all_pdfs():
    for pdf_file in base_dir.rglob("*.pdf"):
        try:
            print(f"Processing {pdf_file.name}...")
            result = process_pdf(pdf_file)
            subject = pdf_file.parent.name.replace(' ', '_')
            filename = f"{subject}.csv"
            filepath = os.path.join(output_folder, filename)
            
            file_exists = os.path.isfile(filepath)

            with open(filepath, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(result["headers"])  # Write headers only if new file
                writer.writerows(result.get("rows", []))  # Always write data rows

            
            print(f"Successfully processed {pdf_file.name} and saved to {filename}.")
        except Exception as e:
            print(f"Failed to process {pdf_file.name}: {e}")
            
            
if __name__ == "__main__":
    process_all_pdfs()
    print("All PDFs processed.")




### TODO: redo Discrete Maths Exam 2022-2023
