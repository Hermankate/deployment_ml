import pdfplumber
import docx2txt
from io import BytesIO
from pdfminer.pdfparser import PDFSyntaxError
import streamlit as st
from pikepdf import Pdf, PdfError

class FileHandler:
    @staticmethod
    def extract_text(file):
        try:
            if file.type == "application/pdf":
                return FileHandler._handle_pdf(file)
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return FileHandler._handle_docx(file)
            return ""
        except Exception as e:
            st.error(f"Error processing {file.name}: {str(e)}")
            return ""

    @staticmethod
    def _handle_pdf(file):
        try:
            # Initial validation
            if file.read(4) != b'%PDF':
                raise PDFSyntaxError("Invalid PDF header")
            file.seek(0)
            
            # Try standard extraction first
            with pdfplumber.open(BytesIO(file.read())) as pdf:
                text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
                if text.strip(): return text
                
            # If empty text, try repaired PDF
            return FileHandler._repair_pdf(file)
            
        except (PDFSyntaxError, PdfError) as e:
            st.warning(f"Corrupted PDF: {file.name}")
            return ""
            
    @staticmethod
    def _repair_pdf(file):
        try:
            repaired = BytesIO()
            with Pdf.open(BytesIO(file.read())) as pdf:
                pdf.save(repaired)
            with pdfplumber.open(repaired) as pdf:
                return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        except Exception:
            return ""

    @staticmethod
    def _handle_docx(file):
        try:
            return docx2txt.process(BytesIO(file.read()))
        except Exception as e:
            st.warning(f"Invalid DOCX: {file.name}")
            return ""