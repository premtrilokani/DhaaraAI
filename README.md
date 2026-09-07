# ⚖️ DhaaraAI (धारा AI) — Indian Legal Assistant Chatbot (RAG)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-green.svg)](https://www.trychroma.com/)
[![Embeddings](https://img.shields.io/badge/Embeddings-all--MiniLM--L6--v2-orange.svg)](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
[![LLM](https://img.shields.io/badge/LLM-Groq%20Llama%203.3%2070B-purple.svg)](https://groq.com/)
[![UI](https://img.shields.io/badge/Frontend-Streamlit-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/Cost-100%25%20Free%20Tier-success.svg)]()

> **An AI-powered Indian legal research assistant built on a Retrieval-Augmented Generation (RAG) architecture. Designed for college project presentation and viva examination.**

---

## 📌 Project Overview

**DhaaraAI** is an AI assistant that explains Indian statutory law (e.g., Indian Penal Code, Bharatiya Nyaya Sanhita, Consumer Protection Act, Constitution) in simple, understandable language for the common Indian citizen.

Unlike generic chatbots (e.g. standard ChatGPT) that hallucinate legal provisions or cite non-existent case laws, DhaaraAI uses **Retrieval-Augmented Generation (RAG)**:
- Answers are strictly grounded in official statutory PDFs (sourced from [indiacode.nic.in](https://www.indiacode.nic.in)).
- Every answer explicitly cites the exact **Section number**, **Act title**, and **source page**.
- Interactive **retrieved sources viewer** allows verification of the raw legal provisions.
- Includes language toggling between **English** and **Hindi (Devanagari)**.
- Operates on **100% free-tier, open-source technology** with zero API billing costs.

---

## 🏗️ End-to-End Architecture

```
                                [ User Question ]
                                       │
                                       ▼
                     ┌───────────────────────────────────┐
                     │     Streamlit Web Application     │
                     │  (Language: English / हिन्दी)     │
                     └─────────────────┬─────────────────┘
                                       │
                                       ▼
                     ┌───────────────────────────────────┐
                     │   Local Sentence-Transformers     │
                     │       (all-MiniLM-L6-v2)          │
                     │  Encodes query -> 384-dim vector  │
                     └─────────────────┬─────────────────┘
                                       │
                                       ▼
                     ┌───────────────────────────────────┐
                     │       Persistent ChromaDB         │
                     │   Collection: 'dhaara_legal_kb'   │
                     │   Cosine Similarity Top-5 Chunks  │
                     └─────────────────┬─────────────────┘
                                       │
                       Retrieved Chunks + Section Metadata
                                       │
                                       ▼
                     ┌───────────────────────────────────┐
                     │    Strict Legal RAG Prompt        │
                     │ • Grounding: context only         │
                     │ • Citation: Act & Section #       │
                     │ • Refusal: "Not enough info"      │
                     │ • Mandatory Legal Disclaimer      │
                     └─────────────────┬─────────────────┘
                                       │
                                       ▼
                     ┌───────────────────────────────────┐
                     │          Groq Cloud API           │
                     │  LLM: llama-3.3-70b-versatile     │
                     │   (Ultra-fast, Free Tier)         │
                     └─────────────────┬─────────────────┘
                                       │
                                       ▼
                       [ Grounded Answer + Source Cards ]
```

---

## 📂 Project Structure

```
d:\DhaaraAI\
├── data/                 # Raw legal PDFs manually downloaded from indiacode.nic.in
│   └── README.txt        # Guidance on where to drop PDFs
├── processed/            # Cached JSON records of extracted, section-tagged chunks
│   └── chunks.json
├── chroma_db/            # Local persistent ChromaDB vector store (SQLite + Parquet)
├── src/
│   ├── __init__.py
│   ├── pdf_loader.py     # Extracts text & page numbers from raw PDFs using pypdf
│   ├── chunker.py        # Token chunking (~500 tokens, 100 overlap) + Section tagging
│   ├── embed_store.py    # Local sentence-transformers (all-MiniLM-L6-v2) + ChromaDB
│   └── rag_engine.py     # Strict RAG query pipeline using Groq's Llama 3.3 70B
├── app/
│   └── app.py            # Streamlit chat interface (English/Hindi, Sources viewer)
├── test_stage1.py        # Verification test for PDF loader & chunker
├── test_stage2.py        # Verification test for local embeddings & ChromaDB
├── test_stage3.py        # Verification test for RAG prompt & Groq Llama 3.3
├── requirements.txt      # Project Python dependencies
├── .env.example          # Template for environment variables
├── .env                  # Secrets configuration (GROQ_API_KEY)
└── README.md             # Project documentation & viva guide
```

---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites
- Python **3.11** or higher installed.
- (Optional but recommended) A free Groq API key from [https://console.groq.com/keys](https://console.groq.com/keys).

### 2. Installation
Open your terminal/PowerShell in the project directory:
```bash
pip install -r requirements.txt
```

### 3. Configure Groq API Key
Copy `.env.example` to `.env` and add your free Groq API key:
```ini
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
```
*(Alternatively, you can leave it blank and enter your API key directly in the Streamlit web sidebar!)*

### 4. Adding Legal Documents
Place any legal acts (PDF format) into the `data/` folder:
- Go to [indiacode.nic.in](https://www.indiacode.nic.in).
- Search and download acts like:
  - *The Indian Penal Code, 1860* (or *Bharatiya Nyaya Sanhita, 2023*)
  - *The Code of Criminal Procedure, 1973* (or *Bharatiya Nagarik Suraksha Sanhita, 2023*)
  - *The Consumer Protection Act, 2019*
  - *The Constitution of India*
- Save the PDF files directly inside the `data/` folder.

### 5. Launch the Streamlit Web Application
Run:
```bash
streamlit run app/app.py
```
Open your browser at `http://localhost:8501`.

Inside the sidebar, click the **"🔄 Index / Refresh PDFs"** button to automatically parse all PDFs in `/data`, chunk them with Section tags, and index them into ChromaDB!

---

## 🧪 Stage Verification Scripts

For testing and demonstration during your project presentation:
- **Test Stage 1 (PDF Loader & Section Chunker)**:
  ```bash
  python test_stage1.py
  ```
- **Test Stage 2 (Embeddings & ChromaDB Storage)**:
  ```bash
  python test_stage2.py
  ```
- **Test Stage 3 (RAG Engine & Guardrail Verification)**:
  ```bash
  python test_stage3.py
  ```

---

## 🎓 College Viva Examination Guide (Q&A)

Here are key questions external examiners and professors frequently ask about this architecture:

### Q1: Why did you use RAG instead of simply asking ChatGPT or fine-tuning an LLM?
> **Answer**:
> 1. **Zero Hallucination**: Standard LLMs hallucinate non-existent sections and penalties. RAG grounds the model to answer *strictly* from the provided statutory text.
> 2. **Verifiability**: RAG provides exact citations (Act name, Section number, page number) so citizens and lawyers can verify the legal provision directly.
> 3. **Maintenance & Cost**: Fine-tuning an LLM on legal text is computationally expensive and becomes outdated when laws are amended. With RAG, updating from IPC to BNS is as simple as dropping new PDFs into `/data` and clicking "Re-index".

### Q2: Why use `all-MiniLM-L6-v2` instead of OpenAI text-embedding-3-small?
> **Answer**:
> - `all-MiniLM-L6-v2` is 100% free, open-source, and runs locally on CPU without sending sensitive document text to any third-party API.
> - Produces compact 384-dimensional dense vectors with ~80MB memory footprint, delivering fast cosine similarity search on standard consumer laptops.

### Q3: Why ChromaDB instead of a traditional SQL database or cloud vector database (Pinecone)?
> **Answer**:
> - Traditional SQL databases perform lexical keyword search (matching exact words), which fails when a citizen asks "punishment for fraud" while the statute uses "cheating and dishonestly inducing delivery of property".
> - ChromaDB performs **semantic vector search** (retrieving concepts even with different phrasing).
> - ChromaDB runs embedded and persistent on local disk (using SQLite and Parquet), requiring zero external server configuration, Docker containers, or paid cloud subscriptions.

### Q4: How does the chunking algorithm preserve legal section boundaries?
> **Answer**:
> - Standard chunkers split blindly on character count, often cutting a legal section in half.
> - DhaaraAI uses token-based chunking (~500 tokens) with a **100-token sliding overlap** to prevent conditions and clauses from being truncated.
> - Regex patterns identify Indian statutory section headers (e.g., `Section 420. Cheating...`), tagging each chunk with its Section number and carrying active sections forward across page boundaries.

### Q5: How do you enforce safety and guardrails in DhaaraAI?
> **Answer**:
> The system prompt enforces four strict guardrails:
> 1. **Grounding**: Must answer strictly using provided context.
> 2. **Citation**: Must cite Act name and Section number.
> 3. **Refusal**: Must output *"I don't have enough information"* if the statutory provision is absent from the database.
> 4. **Disclaimer**: Every response must end with *"This is not legal advice, please consult a lawyer."*

---

## ⚖️ Legal Disclaimer
*DhaaraAI is an academic research and educational college project. It does not provide formal legal advice. Always consult an advocate or qualified legal practitioner for legal counsel.*
