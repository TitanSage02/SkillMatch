import io
from typing import Optional
import pypdf
import docx

class TextExtractor:
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """Extract text from a PDF file content, with OCR fallback for scanned documents."""
        try:
            # First try standard extraction
            pdf_reader = pypdf.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            
            text = text.strip()

            # If no text extracted (scanned PDF), try OCR
            if not text:
                try:
                    import pytesseract
                    from pdf2image import convert_from_bytes
                    
                    # Convert PDF to images
                    images = convert_from_bytes(file_content)
                    
                    # Extract text from each image
                    for image in images:
                        text += pytesseract.image_to_string(image) + "\n"
                    
                    text = text.strip()
                except ImportError:
                    # Log warning but don't fail if OCR libs aren't installed
                    print("Warning: OCR libraries (pytesseract, pdf2image) not found. Skipping OCR.")
                except Exception as e:
                    # Log warning for OCR specific errors ( mfor example missing tesseract binary)
                    print(f"Warning: OCR extraction failed: {str(e)}")

            return text

        except Exception as e:
            raise ValueError(f"Une erreur s'est produite lors de la lecture du PDF: {str(e)}")

    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
        """Extract text from a DOCX file content."""
        try:
            doc = docx.Document(io.BytesIO(file_content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"Une erreur s'est produite lors de la lecture du DOCX: {str(e)}")

    @staticmethod
    def extract_text_from_txt(file_content: bytes) -> str:
        """Extract text from a TXT file content."""
        try:
            return file_content.decode("utf-8").strip()
        except Exception as e:
            raise ValueError(f"Une erreur s'est produite lors de la lecture du fichier texte: {str(e)}")

    @classmethod
    def extract(cls, filename: str, content: bytes) -> str:
        """Main entry point to extract text based on file extension."""
        ext = filename.split('.')[-1].lower()
        
        if ext == 'pdf':
            return cls.extract_text_from_pdf(content)
        elif ext in ['docx', 'doc']:
            return cls.extract_text_from_docx(content)
        elif ext == 'txt':
            return cls.extract_text_from_txt(content)
        else:
            raise ValueError(f"Format de fichier non supporté: {ext}")
