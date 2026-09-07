"""
rag_engine.py
=============
Core Retrieval-Augmented Generation (RAG) engine for DhaaraAI.
Integrates ChromaDB semantic retrieval with Groq's Llama 3.3 70B model.

For College Project / Viva Reference:
-------------------------------------
1. Why RAG (Retrieval-Augmented Generation)?
   - Mitigates Hallucination: Foundation LLMs can invent fake laws, incorrect section
     numbers, or outdated punishments. RAG restricts the LLM to only reason over retrieved,
     verified statutory text.
   - Verifiable Legal Citations: Every answer references specific Sections, Acts, and page numbers.
   - Cost & Freshness: Avoids expensive fine-tuning; when laws are updated (e.g., IPC to BNS),
     we simply update the vector database without retraining any model.
2. Why Groq API & Llama 3.3 70B?
   - Groq LPUs (Language Processing Units) provide ultra-fast token inference (~300-500 tokens/sec).
   - Llama 3.3 70B Versatile is open-weights state-of-the-art with exceptional legal reasoning,
     instruction following, and multilingual (English & Hindi) fluency.
   - Free Tier: Groq offers a generous free tier with zero API billing.
3. Strict System Prompt Enforcement:
   - Grounding: Only answers from retrieved context.
   - Citation: Must cite Section number and Act name.
   - Refusal: Must explicitly say "I don't have enough information" if context is insufficient.
   - Disclaimer: Always appends "This is not legal advice, please consult a lawyer."
   - Multilingual: Fluently answers in English or Hindi (Devanagari) based on user selection.
"""

import os
from typing import List, Dict, Any, Generator, Optional
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Import our persistent ChromaDB store
from embed_store import LegalEmbedStore

# Model configuration
DEFAULT_MODEL = "llama-3.3-70b-versatile"
DISCLAIMER_EN = "This is not legal advice, please consult a lawyer."
DISCLAIMER_HI = "यह कानूनी सलाह नहीं है, कृपया किसी वकील से परामर्श लें।"

SYSTEM_PROMPT_TEMPLATE = """You are DhaaraAI, a dedicated Indian Legal Assistant chatbot designed to help Indian citizens understand their legal rights and statutory provisions in clear, simple language.

You MUST strictly obey the following rules without exception:
1. STRICT GROUNDING: Answer the user's question ONLY using the provided legal context below. Do NOT use outside knowledge, prior assumptions, or unprovided statutes.
2. MANDATORY CITATIONS: Always explicitly cite the statutory Section number (e.g., 'Section 420 of the Indian Penal Code') and the source document/page where the provision is found.
3. INSUFFICIENT INFORMATION REFUSAL: If the provided legal context does not contain enough clear information to answer the question, or if the question is unrelated to the provided context, you MUST answer:
   "I don't have enough information from the provided legal texts to answer this question."
   Do NOT attempt to guess, assume, or fabricate any legal provision.
4. MANDATORY DISCLAIMER: You MUST always conclude your entire answer with this exact disclaimer on a new line:
   "{disclaimer}"
5. LANGUAGE & TONE:
   - Target Language: {language}
   - If English: Use clear, plain English accessible to a common citizen (avoid convoluted legalese while keeping statutory definitions precise).
   - If Hindi: Provide the complete explanation in fluent, respectful Hindi (Devanagari script), while keeping section numbers and statutory acts accurately identified (e.g., 'भारतीय दंड संहिता की धारा 420...').

--- PROVIDED LEGAL CONTEXT ---
{context}
------------------------------
"""


class DhaaraRAGEngine:
    """
    Orchestrates semantic retrieval from ChromaDB and grounded answer generation via Groq.
    """

    def __init__(
        self,
        embed_store: Optional[LegalEmbedStore] = None,
        model_name: str = DEFAULT_MODEL,
        api_key: Optional[str] = None
    ):
        """
        Initializes the RAG Engine with ChromaDB store and Groq client.
        """
        self.embed_store = embed_store or LegalEmbedStore()
        self.model_name = model_name

        # Resolve Groq API key: constructor parameter > os.getenv
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "").strip()
        self.client = None

        if self.api_key:
            self._init_groq_client(self.api_key)
        else:
            print("[rag_engine] Warning: GROQ_API_KEY is not set in .env. Groq client will require API key before querying.")

    def _init_groq_client(self, key: str):
        """
        Initializes Groq client with the given API key.
        """
        try:
            self.api_key = key.strip()
            self.client = Groq(api_key=self.api_key)
            print(f"[rag_engine] Groq client initialized successfully with model '{self.model_name}'.")
        except Exception as e:
            print(f"[rag_engine] Failed to initialize Groq client: {e}")
            self.client = None

    def set_api_key(self, key: str):
        """
        Allows dynamically updating the Groq API key (useful for Streamlit UI).
        """
        self._init_groq_client(key)

    def _format_context(self, chunks: List[Dict[str, Any]]) -> str:
        """
        Formats retrieved ChromaDB chunks into structured context blocks for the prompt.
        """
        if not chunks:
            return "No relevant legal provisions found in the database."

        formatted_blocks = []
        for idx, chunk in enumerate(chunks, 1):
            block = (
                f"[Source Document {idx}]\n"
                f"• Act / File: {chunk.get('source', 'Unknown')}\n"
                f"• Page: {chunk.get('page', 'N/A')}\n"
                f"• Section: {chunk.get('section', 'General')} - {chunk.get('section_title', '')}\n"
                f"• Relevance Score: {chunk.get('similarity_score', 0.0):.4f}\n"
                f"• Statutory Text:\n{chunk.get('text', '').strip()}\n"
            )
            formatted_blocks.append(block)

        return "\n".join(formatted_blocks)

    def query(
        self,
        question: str,
        language: str = "English",
        top_k: int = 5,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Executes end-to-end RAG pipeline:
        1. Retrieves top_k relevant legal chunks from ChromaDB
        2. Formats prompt with strict grounding and citation instructions
        3. Calls Groq Llama 3.3 70B model to generate response

        Parameters:
            question (str): User's legal question.
            language (str): 'English' or 'Hindi'.
            top_k (int): Number of chunks to retrieve (default: 5).
            stream (bool): Whether to return a token generator for streaming UI.

        Returns:
            Dict[str, Any]: {
                "answer": str or Generator,
                "sources": List[Dict],
                "question": str,
                "language": str
            }
        """
        # Step 1: Retrieve top_k chunks from ChromaDB
        retrieved_chunks = self.embed_store.query(question, top_k=top_k)

        # Check if database has any chunks
        if not retrieved_chunks:
            disclaimer = DISCLAIMER_HI if language.lower() == "hindi" else DISCLAIMER_EN
            no_info_msg = (
                "मुझे प्रदान किए गए कानूनी दस्तावेजों से इस प्रश्न का उत्तर देने के लिए पर्याप्त जानकारी नहीं मिली है।"
                if language.lower() == "hindi"
                else "I don't have enough information from the provided legal texts to answer this question."
            )
            return {
                "answer": f"{no_info_msg}\n\n*{disclaimer}*",
                "sources": [],
                "question": question,
                "language": language
            }

        # Step 2: Prepare prompt
        formatted_context = self._format_context(retrieved_chunks)
        disclaimer = DISCLAIMER_HI if language.lower() == "hindi" else DISCLAIMER_EN

        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            disclaimer=disclaimer,
            language=language,
            context=formatted_context
        )

        user_prompt = f"User Question: {question}\n\nPlease provide a clear, cited explanation based strictly on the above context."

        # Step 3: Check API client
        if not self.client:
            if not self.api_key:
                err_msg = (
                    "Groq API Key is not configured. Please set GROQ_API_KEY in your `.env` file or enter it in the sidebar."
                )
                return {
                    "answer": f"{err_msg}\n\n*{disclaimer}*",
                    "sources": retrieved_chunks,
                    "question": question,
                    "language": language
                }
            self._init_groq_client(self.api_key)

        # Step 4: Call Groq Llama 3.3
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        if stream:
            response_stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.1,  # Low temperature for factual precision and zero hallucination
                max_tokens=1024,
                stream=True
            )

            def token_generator():
                for chunk in response_stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content

            return {
                "answer_stream": token_generator(),
                "sources": retrieved_chunks,
                "question": question,
                "language": language
            }
        else:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.1,
                max_tokens=1024,
                stream=False
            )
            answer_text = response.choices[0].message.content.strip()

            # Safeguard: Ensure disclaimer is always present at the end
            if disclaimer not in answer_text:
                answer_text += f"\n\n*{disclaimer}*"

            return {
                "answer": answer_text,
                "sources": retrieved_chunks,
                "question": question,
                "language": language
            }


if __name__ == "__main__":
    # Self-test when executed directly
    engine = DhaaraRAGEngine()
    test_q = "What is the punishment for cheating under Section 420?"
    print(f"\nTesting Query: '{test_q}'")
    result = engine.query(test_q, language="English")
    print("\n--- Answer ---")
    print(result["answer"])
    print("\n--- Retrieved Sources ---")
    for s in result["sources"]:
        print(f"• {s['section']} (Page {s['page']}) - Score: {s['similarity_score']}")
