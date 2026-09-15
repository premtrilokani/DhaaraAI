"""
rag_engine.py
=============
Next-Generation Indian Statutory RAG Engine for DhaaraAI.
Integrates ChromaDB dense semantic retrieval with Groq's Llama 3.3 70B model,
BNS 2023 <-> IPC 1860 Master Concordance, and Supreme Court Landmark Directives.

Design Principles:
1. High Factual Precision: Grounded, citation-backed responses strictly based on statutory law.
2. Zero Outdated Laws: Prioritizes Bharatiya Nyaya Sanhita (BNS 2023) and BNSS 2023, with legacy IPC/CrPC cross-references.
3. Clean IndiaCode Source: Statutory definitions derived from verified IndiaCode legislative texts.
4. Robust Fallbacks: Graceful degradation if vector search finds no matching statute or if Groq API times out/rate-limits.
5. Mandatory Statutory Disclaimer: Appended to every response.
"""

import os
from typing import List, Dict, Any, Generator, Optional
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

from embed_store import LegalEmbedStore
from bns_concordance import diagnose_situation, get_transition_alert
from real_legal_fetcher import RealLegalDataService, OFFICIAL_LEGAL_HELPLINES

DEFAULT_MODEL = "llama-3.3-70b-versatile"
SIMILARITY_THRESHOLD = 0.30

# Mandatory statutory disclaimer appended to all responses
LEGAL_DISCLAIMER = "Ye legal information hai, professional legal advice ka substitute nahi. Kisi advocate se consult karein."

SYSTEM_PROMPT_TEMPLATE = """You are DhaaraAI, an autonomous Indian Legal Intelligence System designed to help Indian citizens understand statutory provisions and procedural safeguards.

CRITICAL STATUTORY RULES:
1. HIGH FACTUAL PRECISION & GROUNDING:
   - Ground all answers in statutory provisions, section numbers, and verified legal definitions.
   - Do NOT guess, fabricate, or assume legal sections.
   - Maintain high factual precision and grounded, citation-backed responses.

2. ACTIVE LAW (BNS 2023 FIRST):
   - In India, criminal statutes were revised effective July 1, 2024.
   - For any offense, ALWAYS cite the ACTIVE statutory section under the Bharatiya Nyaya Sanhita, 2023 (BNS) first (e.g. BNS Section 318(4) for Cheating).
   - ALWAYS also provide the corresponding legacy section under the Indian Penal Code, 1860 (IPC) (e.g. IPC Section 420) for historical cross-referencing.
   - Note the transition rule: Incidents occurring on or after 1 July 2024 are registered under BNS 2023; prior incidents continue under IPC 1860.

3. STRUCTURED ACTIONABLE FORMAT:
   Do NOT use any emojis anywhere in your response.
   Structure your response cleanly using standard markdown headings:
   - **Applicable Legal Provisions (BNS 2023 & IPC)**: Clear section numbers, act names, and exact statutory definitions.
   - **Classification of Offense**:
     • Cognizable or Non-Cognizable (Can police arrest without warrant? Is FIR mandatory?)
     • Bailable or Non-Bailable (Is bail a matter of right or court discretion?)
     • Maximum Punishment (Imprisonment / Fine / Community Service)
     • Triable Court (e.g. Magistrate of First Class / Sessions Court)
   - **Immediate Action Plan**:
     • IF COMPLAINANT / VICTIM: Immediate steps (FIR / Zero FIR under Sec 173 BNSS, National Cybercrime portal 1930, Evidence preservation under Sec 63 BSA certificate).
     • IF ACCUSED / RESPONDENT: Protective safeguards (Section 35(3) BNSS notice rule - no automatic arrest for offenses <= 7 years; Anticipatory Bail under Sec 482 BNSS / 438 CrPC; Right to counsel under Sec 47 BNSS).
   - **Emergency Helplines & Digital Portals**: Relevant helpline numbers (1930 for financial fraud, 112 for police, 181 for women, 1516 for free legal aid).
   - **Legal Disclaimer**: Conclude with: "{disclaimer}"

4. LANGUAGE & TONE:
   - Language: {language}
   - If English: Professional, empathetic, clear, accessible to common citizens.
   - If Hindi: Respectful, fluent Hindi (Devanagari script), retaining statutory sections (e.g. 'भारतीय न्याय संहिता 2023 की धारा 318(4) [पूर्व IPC धारा 420]...').
   - If user asks in Hinglish, explain with clarity so any citizen can understand their rights.

--- VERIFIED STATUTORY CONCORDANCE & LANDMARK GUIDANCE ---
{concordance_context}
---------------------------------------------------------

--- RETRIEVED STATUTORY DATABASE TEXTS (INDIACODE) ---
{retrieved_context}
------------------------------------------------------
"""


class DhaaraRAGEngine:
    """
    Orchestrates semantic retrieval from ChromaDB, BNS 2023 concordance,
    and grounded answer generation via Groq Llama 3.3 70B.
    """

    def __init__(
        self,
        embed_store: Optional[LegalEmbedStore] = None,
        model_name: str = DEFAULT_MODEL,
        api_key: Optional[str] = None
    ):
        self.embed_store = embed_store or LegalEmbedStore()
        self.embed_store.seed_defaults_if_empty()
        self.model_name = model_name
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "").strip()
        self.client = None

        if self.api_key:
            self._init_groq_client(self.api_key)

    def _init_groq_client(self, key: str):
        try:
            self.api_key = key.strip()
            self.client = Groq(api_key=self.api_key)
        except Exception as e:
            print(f"[rag_engine] Failed to initialize Groq client: {e}")
            self.client = None

    def set_api_key(self, key: str):
        self._init_groq_client(key)

    def _format_concordance_context(self, question: str, user_role: str) -> str:
        diagnosis = diagnose_situation(question, user_role=user_role)
        blocks = []

        transition = diagnosis.get("transition", {})
        blocks.append(f"Transition Alert: {transition.get('rule_en', '')}")

        crimes = diagnosis.get("matched_crimes", [])
        for c in crimes:
            b = (
                f"• Offense: {c['offense_en']}\n"
                f"  - Active BNS Section: {c['bns_section']} ({c['bns_act']}) — {c['bns_title']}\n"
                f"  - Legacy IPC Section: {c['ipc_section']} ({c['ipc_act']})\n"
                f"  - Classification: {c['nature']} | {c['bailable']} | Triable by: {c['triable_by']}\n"
                f"  - Punishment: {c['punishment']}\n"
                f"  - BNSS Procedure & Rights: {c['bnss_procedure']}\n"
                f"  - Action for Complainant: {c['victim_guidance']}\n"
                f"  - Safeguard for Accused: {c['accused_guidance']}"
            )
            blocks.append(b)

        guidelines = RealLegalDataService.get_landmark_guidance_for_query(question)
        for g in guidelines:
            gb = (
                f"• Landmark Ruling: {g['case_name']} ({g['governing_statute']})\n"
                f"  Binding Principle: {g['key_rule']}\n"
                f"  Citizen Remedy: {g['citizen_remedy']}"
            )
            blocks.append(gb)

        return "\n\n".join(blocks) if blocks else "General Indian legal statutory inquiry."

    def _format_retrieved_chunks(self, chunks: List[Dict[str, Any]]) -> str:
        if not chunks:
            return "No specific dense text chunks retrieved from IndiaCode repository."

        formatted_blocks = []
        for idx, chunk in enumerate(chunks, 1):
            block = (
                f"[Statute Record {idx}]\n"
                f"• Source: {chunk.get('source', 'IndiaCode')}\n"
                f"• Section: {chunk.get('section', 'General')} - {chunk.get('section_title', '')}\n"
                f"• Relevance: {chunk.get('similarity_score', 0.0):.4f}\n"
                f"• Statutory Text:\n{chunk.get('text', '').strip()}\n"
            )
            formatted_blocks.append(block)

        return "\n".join(formatted_blocks)

    def _generate_offline_concordance_fallback(
        self,
        question: str,
        user_role: str,
        reason: str
    ) -> str:
        """
        Provides graceful offline fallback when Groq API is unavailable or rate-limited.
        """
        diagnosis = diagnose_situation(question, user_role=user_role)
        matched = diagnosis.get("matched_crimes", [])

        lines = [
            f"**Notice**: {reason}",
            "",
            "**Primary Statutory Guidance from Concordance Repository**:",
        ]

        if matched:
            for itm in matched:
                lines.extend([
                    f"### {itm['offense_en']}",
                    f"- **Active Law (BNS 2023)**: Section {itm['bns_section']} ({itm['bns_title']})",
                    f"- **Legacy Law (IPC 1860)**: Section {itm['ipc_section']} ({itm['ipc_title']})",
                    f"- **Nature**: {itm['nature']} | **Bail**: {itm['bailable']}",
                    f"- **Punishment**: {itm['punishment']} | **Trial Court**: {itm['triable_by']}",
                    f"- **Procedure**: {itm['bnss_procedure']}",
                    f"- **Immediate Remedy**: {itm['victim_guidance'] if user_role == 'victim' else itm['accused_guidance']}",
                    ""
                ])
        else:
            lines.extend([
                "Iske liye specific statute nahi mila, general guidance:",
                "1. Cognizable offenses require mandatory First Information Report (FIR) under Section 173 BNSS.",
                "2. For offenses punishable up to 7 years, police must issue a Notice of Appearance under Section 35(3) BNSS before any coercive action.",
                "3. Emergency escalation: Call 112 for Police, 1930 for financial cybercrime fraud, or 1516 for Free Legal Aid (NALSA).",
                ""
            ])

        lines.extend([
            "**Emergency Helplines**:",
            "- National Emergency: 112",
            "- Cyber Crime Financial Fraud: 1930",
            "- Women in Distress: 181",
            "- NALSA Free Legal Aid: 1516",
            "",
            f"*{LEGAL_DISCLAIMER}*"
        ])

        return "\n".join(lines)

    def query(
        self,
        question: str,
        language: str = "English",
        user_role: str = "general",
        top_k: int = 5,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Executes end-to-end situational legal intelligence query with robust fallbacks.
        """
        # 1. Retrieve top_k chunks from ChromaDB
        raw_chunks = self.embed_store.query(question, top_k=top_k)

        # Filter chunks by similarity threshold
        relevant_chunks = [
            c for c in raw_chunks
            if c.get("similarity_score", 0.0) >= SIMILARITY_THRESHOLD
        ]

        # Vector search fallback flag
        vector_fallback_needed = (len(relevant_chunks) == 0)
        fallback_prefix = ""
        if vector_fallback_needed:
            fallback_prefix = "Iske liye specific statute nahi mila, general guidance:\n\n"
            # Keep raw chunks if available for background context, or empty
            used_chunks = raw_chunks[:2] if raw_chunks else []
        else:
            used_chunks = relevant_chunks

        # 2. Build enriched context
        concordance_ctx = self._format_concordance_context(question, user_role)
        retrieved_ctx = self._format_retrieved_chunks(used_chunks)

        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            disclaimer=LEGAL_DISCLAIMER,
            language=language,
            concordance_context=concordance_ctx,
            retrieved_context=retrieved_ctx
        )

        user_prompt = (
            f"Citizen Query / Situation: {question}\n"
            f"User Perspective: {user_role}\n\n"
            f"Please analyze this situation, identify the applicable BNS 2023 & IPC sections, "
            f"classify the offense (bailable/cognizable), and provide the immediate action plan."
        )

        # 3. Check Groq Client Availability
        if not self.client:
            if not self.api_key:
                offline_resp = self._generate_offline_concordance_fallback(
                    question=question,
                    user_role=user_role,
                    reason="Groq API inference key is not configured in .env or sidebar. Showing offline statutory concordance."
                )
                return {
                    "answer": offline_resp,
                    "sources": used_chunks,
                    "question": question,
                    "language": language,
                    "concordance": diagnose_situation(question, user_role)
                }
            self._init_groq_client(self.api_key)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        # 4. Invoke Groq API with robust Try/Except fallback
        try:
            if stream:
                response_stream = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=0.1,  # Low temperature for high factual precision and grounded citation-backed responses
                    max_tokens=1400,
                    stream=True
                )

                def token_generator():
                    if fallback_prefix:
                        yield fallback_prefix
                    for chunk in response_stream:
                        if chunk.choices and chunk.choices[0].delta.content:
                            yield chunk.choices[0].delta.content

                return {
                    "answer_stream": token_generator(),
                    "sources": used_chunks,
                    "question": question,
                    "language": language,
                    "concordance": diagnose_situation(question, user_role)
                }
            else:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=0.1,
                    max_tokens=1400,
                    stream=False
                )
                answer_text = response.choices[0].message.content.strip()

                if fallback_prefix:
                    answer_text = f"{fallback_prefix}{answer_text}"

                # Mandatory Disclaimer enforcement on every response
                if LEGAL_DISCLAIMER not in answer_text:
                    answer_text += f"\n\n*{LEGAL_DISCLAIMER}*"

                return {
                    "answer": answer_text,
                    "sources": used_chunks,
                    "question": question,
                    "language": language,
                    "concordance": diagnose_situation(question, user_role)
                }

        except Exception as api_err:
            print(f"[rag_engine] Groq API call failed: {api_err}. Activating graceful fallback.")
            error_reason = (
                "Groq API connection timeout ya rate limit ke karan live AI inference uplabdh nahi ho saka. "
                "Aapke sawal ke liye statutory concordance aur primary legal provisions neeche uplabdh hain:"
            )
            fallback_text = self._generate_offline_concordance_fallback(
                question=question,
                user_role=user_role,
                reason=error_reason
            )

            return {
                "answer": fallback_text,
                "sources": used_chunks,
                "question": question,
                "language": language,
                "concordance": diagnose_situation(question, user_role)
            }


if __name__ == "__main__":
    engine = DhaaraRAGEngine()
    q = "Someone cheated me online for 50000 rupees through UPI. What case will be filed?"
    print(f"Testing Query: {q}")
    res = engine.query(q)
    print("\nGenerated Response:")
    print(res["answer"])
