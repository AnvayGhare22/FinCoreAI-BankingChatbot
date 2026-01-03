# 🏦 FinCore AI: The Future of Agentic Banking
> **EY Techathon 6.0 | Challenge II: BFSI (Tata Capital)**

![Status](https://img.shields.io/badge/Status-Prototype_Ready-success?style=for-the-badge)
![AI Model](https://img.shields.io/badge/AI-Gemini_1.5_Flash-orange?style=for-the-badge)
![Tech Stack](https://img.shields.io/badge/Stack-Flask_|_Python_|_Deepgram-blue?style=for-the-badge)

**FinCore AI** is an autonomous **Agentic Orchestration Suite** designed to revolutionize the Personal Loan lifecycle. Unlike traditional chatbots, FinCore uses a **Master Agent → Worker Agent** architecture to autonomously handle negotiation, visual KYC verification, risk assessment, and sanction letter generation in real-time.

---

## 🌟 Key Features

* [cite_start]**🧠 Intelligent Orchestration:** A **Master Agent** dynamically delegates tasks to specialized Worker Agents (Sales, Risk, Verification) based on user intent[cite: 69, 72].
* [cite_start]**👁️ Multimodal Vision KYC:** The **Verification Agent** uses Computer Vision (Gemini 1.5 Flash) to scan and verify physical ID cards via the webcam[cite: 89].
* [cite_start]**🗣️ Human-Like Voice Interaction:** Real-time speech-to-text (Deepgram) and neural text-to-speech (Murf AI) for a seamless conversational sales experience[cite: 70].
* [cite_start]**🛡️ UEBA Security Layer:** A built-in **User & Entity Behavior Analytics (UEBA)** monitor logs every agent action to prevent unauthorized data access and ensure compliance[cite: 131, 140, 160].
* [cite_start]**📄 Instant Sanctioning:** The **Sanction Agent** autonomously generates and delivers a signed PDF Sanction Letter upon approval[cite: 98, 76].
* **🎨 Neo-Fintech UI:** A futuristic, glassmorphism-based dashboard that visualizes the "Agent's Brain" activity in real-time.

---

## 🤖 The Agentic Architecture

**FinCore AI** follows a strictly modular **Hub-and-Spoke** architecture as required by the challenge:

| **Agent Role** | **Responsibility** | **Tools & APIs** |
| :--- | :--- | :--- |
| **👑 Master Agent** | The "Brain." [cite_start]Understands intent & orchestrates workers[cite: 78]. | Gemini 1.5 Flash |
| **💼 Sales Agent** | [cite_start]Discusses loan amounts, tenures, and interest rates[cite: 87]. | Knowledge Base |
| **👁️ Verify Agent** | [cite_start]Visualizes ID cards (Pan/Aadhar) for KYC compliance[cite: 89]. | Computer Vision |
| **⚖️ Risk Agent** | [cite_start]Fetches Credit Scores & assesses eligibility logic[cite: 92]. | Mock Bureau API |
| **📝 Sanction Agent** | [cite_start]Generates the final approval letter[cite: 98]. | FPDF / DocGen |
| **🔒 UEBA Monitor** | [cite_start]Logs anomalies and authorizes API calls[cite: 145]. | Security Logic |

---

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3 (Glassmorphism), Vanilla JS (MediaRecorder API).
* **Backend:** Python, Flask.
* **AI Engine:** Google Gemini 1.5 Flash (Orchestration & Vision).
* **Voice Pipeline:**
    * *Input:* Deepgram Nova-2 (High-speed Transcription).
    * *Output:* Murf AI (Neural TTS).
* **Utilities:** `FPDF` (PDF Generation), `Dotenv` (Config).

---

## 🚀 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/yourusername/fincore-ai.git](https://github.com/yourusername/fincore-ai.git)
    cd fincore-ai
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Ensure you have `flask`, `google-generativeai`, `requests`, `python-dotenv`, `fpdf` installed)*

3.  **Configure Environment Variables**
    Create a `.env` file in the root directory and add your API keys:
    ```env
    GEMINI_API_KEY=your_gemini_key
    MURF_API_KEY=your_murf_key
    DEEPGRAM_API_KEY=your_deepgram_key
    ```

4.  **Run the Application**
    ```bash
    python app.py
    ```

5.  **Access the Dashboard**
    Open your browser and navigate to: `http://127.0.0.1:5000`

---

## 🎮 How to Demo 

To experience the full capability of the Agentic System:

1.  **Login:** Start at the secure `login.html` page.
2.  **Voice Command:** Click the Orb and say: *"I want to apply for a personal loan."* -> *Observe the **Sales Agent** lighting up.*
3.  **Risk Check:** Say: *"Am I eligible?"* -> *Observe the **Underwriting Agent** checking your (mock) credit score.*
4.  **Vision KYC:** Click **"Enable KYC Vision"**, hold up an ID card to the camera, and say: *"Scan my ID."* -> *Observe the **Verification Agent** confirming your identity.*
5.  **Sanction:** Say: *"Generate my sanction letter."* -> *The system generates a **PDF**, and a Download button appears.*
6.  **Security Check:** Point to the **UEBA Log** at the bottom right to verify that every step was logged for compliance.

---

## 👥 Team

* **Anvay Ghare**
* **Mitali Jichkar**
* **Ekata Mukewar**
* **Utkarsh Mundhada**
* **Tanisha Chaudhary**   

---

> *"Banking is necessary, banks are not." - Bill Gates*
>
> **FinCore AI** makes banking invisible, instant, and intelligent.
