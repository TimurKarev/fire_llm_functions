import io

from firebase_admin.storage import bucket as bucket_type
from PyPDF2 import PdfReader


def get_file_from_firestore(bucket: bucket_type, path: str) -> io.BytesIO:
    pdf_file = io.BytesIO()
    bucket.blob(path).download_to_file(pdf_file)
    pdf_file.seek(0)

    return pdf_file


def get_text_from_pdf_file(pdf_file: io.BytesIO) -> str:
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    return text
