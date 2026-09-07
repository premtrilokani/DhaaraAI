"""
test_stage1.py
==============
Verification script for Stage 1:
1. Tests PDF loading with pypdf
2. Tests token-based chunking (~500 tokens, 100 token overlap)
3. Tests legal section detection and tagging (e.g. 'Section 415', 'Section 420')
4. Checks metadata tagging (source, page, section, section title, token count)
"""

import sys
import os
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pdf_loader import load_pdf, load_all_pdfs, clean_text
from chunker import split_text_by_tokens, detect_sections, process_pages_into_chunks, count_tokens


def create_sample_pdf_if_needed(output_path: str):
    """
    Creates a minimal legal sample PDF using reportlab for local verification
    if the user hasn't added PDFs yet.
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(output_path, pagesize=letter)
        
        # Page 1
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 750, "THE INDIAN PENAL CODE, 1860")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 725, "CHAPTER XVII - OF OFFENCES AGAINST PROPERTY")
        
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, 695, "Section 415. Cheating")
        c.setFont("Helvetica", 10)
        text_p1 = (
            "Whoever, by deceiving any person, fraudulently or dishonestly induces the person so deceived "
            "to deliver any property to any person, or to consent that any person shall retain any property, "
            "or intentionally induces the person so deceived to do or omit to do anything which he would not do "
            "or omit if he were not so deceived, and which act or omission causes or is likely to cause damage or "
            "harm to that person in body, mind, reputation or property, is said to 'cheat'.\n\n"
            "Explanation.—A dishonest concealment of facts is a deception within the meaning of this section."
        )
        text_obj = c.beginText(50, 675)
        text_obj.setFont("Helvetica", 10)
        for line in text_p1.split("\n"):
            text_obj.textLine(line)
        c.drawText(text_obj)
        c.showPage()

        # Page 2
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, 750, "Section 420. Cheating and dishonestly inducing delivery of property")
        c.setFont("Helvetica", 10)
        text_p2 = (
            "Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to "
            "any person, or to make, alter or destroy the whole or any part of a valuable security, or anything "
            "which is signed or sealed, and which is capable of being converted into a valuable security, shall "
            "be punished with imprisonment of either description for a term which may extend to seven years, "
            "and shall also be liable to fine.\n\n"
            "Section 421. Dishonest or fraudulent removal or concealment of property to prevent distribution among creditors.\n"
            "Whoever dishonestly or fraudulently removes, conceals or delivers to any person, or transfers or causes "
            "to be transferred to any person, without adequate consideration, any property, intending thereby to prevent, "
            "or knowing it to be likely that he will thereby prevent, the distribution of that property according to law "
            "among his creditors, or the creditors of any other person, shall be punished with imprisonment of either "
            "description for a term which may extend to two years, or with fine, or with both."
        )
        text_obj2 = c.beginText(50, 730)
        text_obj2.setFont("Helvetica", 10)
        for line in text_p2.split("\n"):
            text_obj2.textLine(line)
        c.drawText(text_obj2)
        c.showPage()
        
        c.save()
        print(f"[test_stage1] Generated sample verification PDF at: {output_path}")
        return True
    except Exception as e:
        print(f"[test_stage1] Could not generate sample PDF: {e}")
        return False


def run_stage1_verification():
    print("=" * 60)
    print("DHAARAAI STAGE 1 VERIFICATION: PDF Loader & Chunker")
    print("=" * 60)

    # Step 1: Check for PDFs in data/
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    pdf_files = list(data_dir.glob("*.pdf"))

    sample_created = False
    if not pdf_files:
        sample_path = data_dir / "sample_ipc_sections.pdf"
        print("[test] No user PDFs found in /data yet. Creating a sample legal PDF for test verification...")
        sample_created = create_sample_pdf_if_needed(str(sample_path))
        if sample_created:
            pdf_files = [sample_path]

    # Step 2: Load PDF(s)
    print(f"\n--- 1. Testing PDF Loader (Found {len(pdf_files)} PDF file(s)) ---")
    pages = load_all_pdfs(str(data_dir))
    assert len(pages) > 0, "No pages extracted! Check PDF loading logic."
    print(f"-> Extracted {len(pages)} page(s) successfully.")
    for p in pages:
        print(f"   [Source: {p['source']} | Page: {p['page']} | Text Length: {len(p['text'])} chars]")

    # Step 3: Test Section Detection
    print("\n--- 2. Testing Section Detection Engine ---")
    sample_text = pages[0]["text"]
    sections_found = detect_sections(sample_text)
    print(f"-> Sections detected in Page 1 text: {sections_found}")

    # Step 4: Process into Chunks (~500 tokens, 100 overlap)
    print("\n--- 3. Testing Token Chunking & Section Tagging ---")
    chunks = process_pages_into_chunks(pages, chunk_size=500, overlap=100, save_to_file="processed/chunks.json")
    assert len(chunks) > 0, "No chunks generated!"
    print(f"-> Total chunks created: {len(chunks)}")

    print("\n--- 4. Inspecting Chunk Records & Metadata ---")
    for idx, c in enumerate(chunks, 1):
        print(f"\n[Chunk #{idx}]")
        print(f"  • Chunk ID      : {c['chunk_id']}")
        print(f"  • Source File   : {c['source']}")
        print(f"  • Page Number   : {c['page']}")
        print(f"  • Tagged Section: {c['section']}")
        print(f"  • Section Title : {c['section_title']}")
        print(f"  • Token Count   : {c['token_count']}")
        print(f"  • Preview Text  :\n    \"{c['text'][:160]}...\"")

    print("\n" + "=" * 60)
    print("STAGE 1 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    run_stage1_verification()
