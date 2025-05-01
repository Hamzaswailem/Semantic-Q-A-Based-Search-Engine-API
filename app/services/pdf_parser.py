from PyPDF2 import PdfReader
from typing import BinaryIO
from langchain.text_splitter import RecursiveCharacterTextSplitter

class Parser:
    #Text Extractor
    @staticmethod   
    #File type is BinaryIO
    def extract_text(file: BinaryIO) -> str:
        reader = PdfReader(file)  
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text

    #Chunking textsss
    @staticmethod
    #File type is string
    def chunk_text(text: str):   
        text_splitter = RecursiveCharacterTextSplitter( 
            chunk_size=500,
            chunk_overlap=100,      # To avoid overlaping
            length_function=len,
            separators=["\n\n", "\n", " ", ""]       
        )
        
        
        chunks = text_splitter.split_text(text)
        return chunks