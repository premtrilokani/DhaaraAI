"""
chunker.py
==========
Module responsible for splitting extracted document text into semantic chunks
with token-based overlap and Indian legal Section tagging.

For College Project / Viva Reference:
-------------------------------------
1. Why Token Chunking (~500 tokens, 100 overlap)?
   - Large Language Models (LLMs) and vector embedding models process text in tokens.
   - 500 tokens (~350-400 English words) is an ideal semantic size for legal provisions:
     it is large enough to contain an entire legal section (definition, explanation,
     exceptions, and punishment) without fragmenting the reasoning.
   - 100 tokens of overlap prevents the "boundary problem" where a crucial phrase
     (e.g., "Provided that nothing herein shall apply...") is sliced across chunks.
2. Section Tagging:
   - Indian statutes (IPC, CrPC, BNS, CPC, Evidence Act) are organized by numbered Sections.
   - Legal users think and query in terms of Sections (e.g., "What is the bail condition in Section 437?").
   - By tagging each chunk with its Section number and carrying active sections across boundaries,
     the RAG engine can provide exact legal citations to the LLM and the end user.
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    import tiktoken
    _TIKTOKEN_AVAILABLE = True
    _ENCODER = tiktoken.get_encoding("cl100k_base")
except ImportError:
    _TIKTOKEN_AVAILABLE = False
    _ENCODER = None


# Regular expression patterns to identify Indian Legal Sections:
# 1. Matches: "Section 420", "Sec. 420", "Section 302.", "Section 498A - Cruelty..."
REGEX_SECTION_EXPLICIT = re.compile(
    r'(?i)\b(?:Section|Sec\.?)\s*([0-9]+[A-Z]?(?:\s*\([a-zA-Z0-9]+\))*)\s*[-.:–—]?\s*([^\n\r\.\;]*)'
)

# 2. Matches numbered sections at start of lines, e.g.: "420. Cheating and dishonestly..."
REGEX_SECTION_NUMBERED_LINE = re.compile(
    r'(?m)^\s*([0-9]{1,4}[A-Z]?)\.\s+([A-Z][^\n\r\.\;]{3,80})'
)


def count_tokens(text: str) -> int:
    """
    Returns the token count of a given text using tiktoken (cl100k_base),
    or falls back to an approximate word/char count if tiktoken is not yet installed.
    """
    if _TIKTOKEN_AVAILABLE and _ENCODER:
        return len(_ENCODER.encode(text))
    # Fallback approximation: 1 token ≈ 4 characters or 0.75 words
    return max(1, len(text.split()) * 4 // 3)


def detect_sections(text: str) -> List[Dict[str, str]]:
    """
    Detects all legal Section references in a block of text.

    Returns a list of dicts:
        [
            {"section": "Section 420", "title": "Cheating and dishonestly inducing delivery of property"},
            ...
        ]
    """
    detected = []
    seen = set()

    # Check explicit "Section 123" patterns
    for match in REGEX_SECTION_EXPLICIT.finditer(text):
        sec_num = match.group(1).strip()
        sec_title = match.group(2).strip()
        formatted_sec = f"Section {sec_num}"
        if formatted_sec not in seen:
            seen.add(formatted_sec)
            detected.append({
                "section": formatted_sec,
                "title": sec_title[:120] if sec_title else ""
            })

    # Check numbered line patterns ("420. Cheating...")
    for match in REGEX_SECTION_NUMBERED_LINE.finditer(text):
        sec_num = match.group(1).strip()
        sec_title = match.group(2).strip()
        formatted_sec = f"Section {sec_num}"
        if formatted_sec not in seen:
            seen.add(formatted_sec)
            detected.append({
                "section": formatted_sec,
                "title": sec_title[:120] if sec_title else ""
            })

    return detected


def split_text_by_tokens(text: str, chunk_size: int = 500, overlap: int = 100) -> List[Dict[str, Any]]:
    """
    Splits text into chunks of approximately `chunk_size` tokens with `overlap` tokens.
    Uses tiktoken BPE when available for exact token boundaries, decoding back to clean strings.
    """
    if not text.strip():
        return []

    if _TIKTOKEN_AVAILABLE and _ENCODER:
        tokens = _ENCODER.encode(text)
        total_tokens = len(tokens)

        if total_tokens <= chunk_size:
            return [{"text": text, "token_count": total_tokens}]

        step = chunk_size - overlap
        chunks = []
        start = 0

        while start < total_tokens:
            end = min(start + chunk_size, total_tokens)
            chunk_tokens = tokens[start:end]
            chunk_text = _ENCODER.decode(chunk_tokens).strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "token_count": len(chunk_tokens)
                })

            if end >= total_tokens:
                break
            start += step

        return chunks
    else:
        # Fallback word-based chunking (~1.3 words per token, so 500 tokens ~ 380 words)
        words = text.split()
        words_per_chunk = int(chunk_size * 0.75)
        words_overlap = int(overlap * 0.75)
        step = max(1, words_per_chunk - words_overlap)

        chunks = []
        for i in range(0, len(words), step):
            chunk_words = words[i:i + words_per_chunk]
            chunk_text = " ".join(chunk_words).strip()
            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "token_count": count_tokens(chunk_text)
                })
            if i + words_per_chunk >= len(words):
                break
        return chunks


def process_pages_into_chunks(
    pages: List[Dict[str, Any]],
    chunk_size: int = 500,
    overlap: int = 100,
    save_to_file: Optional[str] = "processed/chunks.json"
) -> List[Dict[str, Any]]:
    """
    Transforms raw page-level records into tagged, section-aware chunks.

    Parameters:
        pages (List[Dict[str, Any]]): Extracted pages from pdf_loader.
        chunk_size (int): Target token count per chunk (~500).
        overlap (int): Token overlap between consecutive chunks (~100).
        save_to_file (str, optional): Destination JSON path in /processed.

    Returns:
        List[Dict[str, Any]]: Complete list of enriched chunk dictionaries.
    """
    all_chunks = []
    chunk_counter = 0

    # Stateful section tracking across documents
    current_section = "General / Preamble"
    current_title = ""
    current_source = ""

    for page_item in pages:
        source = page_item.get("source", "unknown_doc")
        page_num = page_item.get("page", 1)
        page_text = page_item.get("text", "")

        # Reset section state if moving to a new document
        if source != current_source:
            current_source = source
            current_section = "General / Preamble"
            current_title = ""

        # Break page text into token chunks
        raw_chunks = split_text_by_tokens(page_text, chunk_size=chunk_size, overlap=overlap)

        for rc in raw_chunks:
            chunk_counter += 1
            chunk_text = rc["text"]
            token_count = rc["token_count"]

            # Detect sections in this specific chunk
            sections_found = detect_sections(chunk_text)

            if sections_found:
                # Update current section to the primary (first) section detected in this chunk
                primary_section = sections_found[0]["section"]
                primary_title = sections_found[0]["title"]
                current_section = primary_section
                current_title = primary_title
                all_sections_in_chunk = [s["section"] for s in sections_found]
            else:
                # Inherit previous active section (Section is continued across pages/chunks)
                primary_section = current_section
                primary_title = current_title
                all_sections_in_chunk = [current_section] if current_section != "General / Preamble" else []

            chunk_id = f"{Path(source).stem}_p{page_num}_c{chunk_counter}"

            chunk_record = {
                "chunk_id": chunk_id,
                "source": source,
                "page": page_num,
                "section": primary_section,
                "section_title": current_title,
                "all_sections": all_sections_in_chunk,
                "token_count": token_count,
                "text": chunk_text
            }
            all_chunks.append(chunk_record)

    # Save to /processed cache if path is provided
    if save_to_file and all_chunks:
        out_path = Path(save_to_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, indent=2, ensure_ascii=False)
        print(f"[chunker] Saved {len(all_chunks)} processed chunks to '{save_to_file}'.")

    return all_chunks


if __name__ == "__main__":
    # Self-test with sample legal snippet
    sample_legal_text = (
        "CHAPTER XVII\nOF OFFENCES AGAINST PROPERTY\n\n"
        "Section 415. Cheating.—Whoever, by deceiving any person, fraudulently or dishonestly induces the person so "
        "deceived to deliver any property to any person, or to consent that any person shall retain any property, or "
        "intentionally induces the person so deceived to do or omit to do anything which he would not do or omit if he "
        "were not so deceived, and which act or omission causes or is likely to cause damage or harm to that person in body, "
        "mind, reputation or property, is said to 'cheat'.\n\n"
        "Explanation.—A dishonest concealment of facts is a deception within the meaning of this section.\n\n"
        "Section 420. Cheating and dishonestly inducing delivery of property.—Whoever cheats and thereby dishonestly induces "
        "the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a "
        "valuable security, or anything which is signed or sealed, and which is capable of being converted into a valuable security, "
        "shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine."
    )

    mock_pages = [{"page": 1, "source": "IPC_Sample.pdf", "text": sample_legal_text}]
    chunks = process_pages_into_chunks(mock_pages, chunk_size=100, overlap=25, save_to_file="processed/chunks_test.json")

    print(f"\nTest Result: Processed {len(chunks)} chunks.")
    for c in chunks:
        print(f"\n--- Chunk ID: {c['chunk_id']} | Tagged Section: {c['section']} ({c['section_title']}) | Tokens: {c['token_count']} ---")
        print(c['text'][:140] + "...")
