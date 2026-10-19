import os
from PyPDF2 import PdfReader
from fastapi import HTTPException

def extract_text_from_txt(file_path:str)->str:
    """
    Extracts the text from txt file

    Args:
        file path (str): The path to the TXT file
    """
    with open(file_path,"r",encoding="utf-8") as f:
        return f.read()

def extract_text_from_pdf(file_path:str) -> str:
    """
    Extracts text from PDF file

    Args:
        file path (str): The path to the PDF file
    """

    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return {"text": text.strip(),"page_count":str(len(reader.pages)),"word_count":str(len(text.split()))}

def extract_text(file_path:str)->str:
    """
    Extracts text from a document file

    Args:
        file_path (str): The path to the document file
    """

    ext = os.path.splitext(file_path)[1].lower()
    print(f"---> {ext}")
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise HTTPException(status_code=400,detail="Unsupported file type. Only PDF and TXT files are allowed")