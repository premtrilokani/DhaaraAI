"""
pdf_loader.py
=============
Module responsible for loading legal documents (PDFs) from the raw data folder.

For College Project / Viva Reference:
-------------------------------------
1. Why PDF Extraction?
   Legal acts (like IPC, CrPC, BNS, Indian Evidence Act) from repositories like
   indiacode.nic.in are officially published in PDF format.
2. Why pypdf?
   pypdf is a pure-Python library requiring no external binary dependencies or C++
   compilers, making it completely platform-independent, lightweight, and fast.
3. Metadata Preservation:
   Extracting text page-by-page allows us to attach 'page' and 'source' metadata
   to every chunk. In legal research, citing the exact page and source document
   is vital for auditability and verification.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any
from pypdf import PdfReader


def clean_text(text: str) -> str:
    """
    Cleans extracted raw PDF text to improve chunking and embedding quality.
    
    Operations:
    - Removes zero-width and non-printable control characters.
    - Joins words broken across lines by hyphens (e.g., 'punish-\\nment' -> 'punishment').
    - Normalizes repeated whitespaces and tabs into single spaces while preserving paragraph breaks.
    """
    if not text:
        return ""

    # Replace carriage returns with standard newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Fix words hyphenated across line breaks (e.g., "infor-\nmation" -> "information")
    text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

    # Replace multiple consecutive spaces/tabs on the same line with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Collapse more than two consecutive newlines into two newlines (clean paragraphs)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def load_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Extracts text page-by-page from a single PDF file.

    Parameters:
        pdf_path (str): File system path to the PDF document.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dict represents a page:
            {
                "page": int (1-indexed),
                "source": str (filename),
                "text": str (cleaned page content)
            }
    """
    path_obj = Path(pdf_path)
    if not path_obj.exists() or not path_obj.is_file():
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

    filename = path_obj.name
    pages_data = []

    try:
        reader = PdfReader(str(path_obj))
        total_pages = len(reader.pages)
        print(f"[pdf_loader] Reading '{filename}' ({total_pages} pages)...")

        for idx, page in enumerate(reader.pages):
            page_number = idx + 1
            raw_text = page.extract_text() or ""
            cleaned = clean_text(raw_text)

            # Keep page even if text is short, but record non-empty text
            if cleaned:
                pages_data.append({
                    "page": page_number,
                    "source": filename,
                    "text": cleaned
                })

        print(f"[pdf_loader] Successfully extracted {len(pages_data)} pages from '{filename}'.")
    except Exception as e:
        print(f"[pdf_loader] Error reading '{filename}': {e}")
        raise e

    return pages_data


def load_all_pdfs(data_dir: str = "data") -> List[Dict[str, Any]]:
    """
    Scans the specified directory for all PDF files and extracts text from each.

    Parameters:
        data_dir (str): Directory containing legal PDFs (default: 'data').

    Returns:
        List[Dict[str, Any]]: Aggregated list of page-level records from all PDFs.
    """
    dir_path = Path(data_dir)
    if not dir_path.exists():
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"[pdf_loader] Created directory '{data_dir}'. Please drop your legal PDFs here.")
        return []

    pdf_files = list(dir_path.glob("*.pdf"))
    if not pdf_files:
        print(f"[pdf_loader] No PDF files found in '{data_dir}'.")
        return []

    print(f"[pdf_loader] Found {len(pdf_files)} PDF(s) in '{data_dir}': {[f.name for f in pdf_files]}")

    all_pages = []
    for pdf_file in pdf_files:
        try:
            pages = load_pdf(str(pdf_file))
            all_pages.extend(pages)
        except Exception as err:
            print(f"[pdf_loader] Skipping '{pdf_file.name}' due to error: {err}")

    print(f"[pdf_loader] Total extracted pages across all documents: {len(all_pages)}")
    return all_pages


if __name__ == "__main__":
    # Self-test when executed directly
    print("Testing pdf_loader module...")
    pages = load_all_pdfs("data")
    print(f"Total pages loaded: {len(pages)}")
