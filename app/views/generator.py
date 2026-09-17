"""
generator.py
============
Document Generator view logic.
"""
import streamlit as st
from datetime import datetime

def render_generator():
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="font-size: 20px; font-weight: 700; color: #111; margin: 0 0 4px 0;">Statutory Legal Draft Generator</h2>
        <p style="font-size: 14px; color: #666; margin: 0;">
            Generate formal legal notices and applications with verified statutory references under BNSS Section 173 or Section 138 NI Act.
        </p>
    </div>
    """, unsafe_allow_html=True)

    draft_choice = st.selectbox(
        "Select Document Type:",
        [
            "First Information Report Application (Section 173 BNSS)",
            "Statutory Demand Notice for Dishonour of Cheque (Section 138 NI Act)",
            "Cyber Financial Fraud Reporting Application"
        ]
    )

    st.write("")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        complainant_name = st.text_input("Complainant Name:", value="Rajesh Kumar")
        complainant_contact = st.text_input("Contact Details & Address:", value="+91-9876543210, New Delhi")
        incident_date = st.date_input("Date of Incident:", value=datetime.today())
        police_station = st.text_input("Police Station / Jurisdiction:", value="Cyber Crime Police Station")

    with col_d2:
        accused_name = st.text_input("Accused / Opposite Party:", value="Person X / Organization ABC")
        loss_amount = st.text_input("Amount or Subject Matter:", value="Rs. 50,000/-")
        facts = st.text_area(
            "Summary of Facts:",
            value="The accused deceived the complainant into transferring funds on false pretenses, following which communications were ceased and obligations breached.",
            height=120
        )

    st.write("")
    
    st.markdown("""
    <style>
    div[data-testid="stButton"] button {
        background: #000000 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        padding: 12px !important;
    }
    div[data-testid="stButton"] button:hover {
        background: #222 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if st.button("Generate Document", use_container_width=True):
        if "Section 173 BNSS" in draft_choice:
            draft_text = f"""TO,
THE OFFICER IN CHARGE / STATION HOUSE OFFICER,
{police_station.upper()}

SUBJECT: APPLICATION UNDER SECTION 173 BHARATIYA NAGARIK SURAKSHA SANHITA, 2023 (BNSS) FOR REGISTRATION OF FIRST INFORMATION REPORT (F.I.R.)

Respected Sir/Madam,

I, {complainant_name}, residing at {complainant_contact}, do hereby submit this formal complaint as follows:

1. That on {incident_date.strftime('%d-%m-%Y')}, an offense occurred within the territorial jurisdiction of this Police Station.

2. ACCUSED DETAILS:
   Name / Identity: {accused_name}

3. STATEMENT OF FACTS:
   {facts}
   Total Financial / Material Loss: {loss_amount}

4. APPLICABLE STATUTORY PROVISIONS:
   The acts committed by the accused disclose the commission of cognizable offenses under:
   - Section 318(4) of the Bharatiya Nyaya Sanhita, 2023 (Cheating and dishonestly inducing delivery of property) [Corresponds to Section 420 IPC].
   - Section 316 of the Bharatiya Nyaya Sanhita, 2023 (Criminal Breach of Trust) [Corresponds to Section 406 IPC].
   - Relevant provisions of the Information Technology Act, 2000.

5. PRAYER:
   In view of the binding mandate of the Supreme Court in Lalita Kumari v. Govt. of U.P. and Section 173(1) BNSS, you are requested to:
   (a) Register a First Information Report (F.I.R.) immediately.
   (b) Furnish a copy of the registered F.I.R. free of cost as mandated by Section 173(2) BNSS.
   (c) Initiate an investigation in accordance with law.

Yours faithfully,

Date: {datetime.today().strftime('%d-%m-%Y')}
Place: {police_station}
Signature: __________________________
Name: {complainant_name}
Mobile: {complainant_contact}

ENCLOSURES (Admissibility under Section 63 Bharatiya Sakshya Adhiniyam):
1. Copy of Bank Statement / Transaction Slips.
2. Electronic communications / WhatsApp transcripts.
3. Identity Verification Document.
"""
        elif "Section 138" in draft_choice:
            draft_text = f"""REGISTERED POST WITH ACKNOWLEDGEMENT DUE / STATUTORY NOTICE

Date: {datetime.today().strftime('%d-%m-%Y')}

TO,
{accused_name}
[Full Address of the Drawer]

SUBJECT: LEGAL NOTICE UNDER SECTION 138 OF THE NEGOTIABLE INSTRUMENTS ACT, 1881 FOR DISHONOUR OF CHEQUE FOR AMOUNT {loss_amount}.

Sir / Madam,

Under instructions from my client, {complainant_name} (Address: {complainant_contact}), I hereby serve upon you this Statutory Legal Demand Notice:

1. That in discharge of a legally enforceable debt/liability, you issued Cheque bearing No. [Insert Cheque Number] drawn on [Bank Name] for an amount of {loss_amount} in favour of my client.

2. That the said cheque was presented for clearance within its validity period. However, the said cheque was returned unpaid by the bank vide Return Memo dated {incident_date.strftime('%d-%m-%Y')} with the remarks: "FUNDS INSUFFICIENT / EXCEEDS ARRANGEMENT".

3. FACTUAL SUMMARY:
   {facts}

4. That by dishonouring the said cheque, you have committed an offense punishable under Section 138 of the Negotiable Instruments Act, 1881.

5. DEMAND:
   I hereby demand that you pay the full amount of {loss_amount} to my client within FIFTEEN (15) DAYS of receipt of this notice.

6. Failure to comply with this notice within 15 days shall leave my client with no option but to initiate criminal proceedings against you under Section 138 of the Negotiable Instruments Act and Section 318(4) of the Bharatiya Nyaya Sanhita, 2023 before the competent Court of Judicial Magistrate.

Advocate for Complainant
Signature: ______________________
"""
        else:
            draft_text = f"""NATIONAL CYBER CRIME REPORTING PORTAL (cybercrime.gov.in / 1930)
OFFICIAL INCIDENT DOSSIER

Category: Cyber Financial Fraud / Identity Deception
Date of Incident: {incident_date.strftime('%d-%m-%Y')}
Complainant: {complainant_name} | {complainant_contact}
Suspect Details: {accused_name}
Total Disputed Amount: {loss_amount}

SUMMARY OF INCIDENT:
{facts}

EVIDENCE RECORD UNDER SECTION 63 BHARATIYA SAKSHYA ADHINIYAM (BSA 2023):
- Transaction Reference Numbers (UTR)
- Bank Account Debit Record
- Electronic Communication Logs and IP Records
- Device Authenticity Certificate under Section 63 BSA

RELIEF SOUGHT:
Immediate freezing of beneficiary accounts through the 1930 Citizen Financial Cyber Fraud Reporting System and registration of case under Section 318(4) BNS 2023 read with Sections 66C and 66D of the Information Technology Act, 2000.
"""

        st.markdown('<div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: #888; margin: 24px 0 8px 0;">Generated Document</div>', unsafe_allow_html=True)
        st.code(draft_text, language="text")
        st.download_button(
            label="Download Document (.txt)",
            data=draft_text,
            file_name=f"Legal_Notice_{complainant_name.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
