import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
import requests
import base64
import json
import random
from fpdf import FPDF
from datetime import datetime

# --- 1. SETUP ---
basedir = os.path.abspath(os.path.dirname(__file__))  
env_path = os.path.join(basedir, '.env')
load_dotenv(env_path)

app = Flask(__name__, static_folder='templates', static_url_path='')

# Load Keys
gemini_key = os.getenv("GEMINI_API_KEY")
murf_key = os.getenv("MURF_API_KEY")
deepgram_key = os.getenv("DEEPGRAM_API_KEY")

if gemini_key:
    genai.configure(api_key=gemini_key)

# API Constants
MURF_STREAM_URL = "https://api.murf.ai/v1/speech/stream"
DEEPGRAM_API_URL = "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true"

# --- 2. MOCK BANKING DATA & TOOLS ---
def get_mock_credit_score():
    """Simulates fetching data from a Credit Bureau (Experian/CIBIL)"""
    return {
        "score": random.randint(720, 850),
        "limit": 500000,
        "name": "Anvay Ghare"
    }

def generate_sanction_pdf(amount, name):
    """Generates a physical Sanction Letter PDF"""
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(10, 37, 64) # Tata Navy
    pdf.cell(200, 10, txt="TATA CAPITAL - SANCTION LETTER", ln=1, align='C')
    pdf.ln(10)
    
    # Body
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    date_str = datetime.now().strftime("%d-%m-%Y")
    
    content = [
        f"Date: {date_str}",
        f"Applicant: {name}",
        "",
        "Subject: In-Principle Sanction of Personal Loan",
        "",
        "Dear Customer,",
        f"Based on your automated credit check and AI verification,",
        f"we are pleased to approve a Personal Loan of:",
        "",
        f"   INR {amount} /-",
        "",
        "Terms & Conditions:",
        "- Interest Rate: 10.99% p.a.",
        "- Tenure: 36 Months",
        "- Agent: FinCore AI Master Agent",
        "",
        "Sincerely,",
        "Tata Capital AI Team"
    ]
    
    for line in content:
        pdf.cell(200, 10, txt=line, ln=1, align='L')
        
    filename = "Sanction_Letter.pdf"
    filepath = os.path.join(basedir, filename)
    pdf.output(filepath)
    return filename

# --- 3. ROUTES --- 
@app.route('/')
def home(): return render_template('homepage.html')

@app.route('/login.html')
def login_page(): return render_template('login.html')

@app.route('/download_pdf')
def download_pdf():
    path = os.path.join(basedir, "Sanction_Letter.pdf")
    return send_file(path, as_attachment=True)

# --- 4. CORE AI ENGINE (VOICE + VISION + TEXT + UEBA) ---

@app.route('/process_audio', methods=['POST'])
def process_audio():
    print("\n--- DEBUG: STARTING REQUEST ---")
    
    # 1. INPUT HANDLING
    transcript = ""
    image_part = None
    
    # Check for text input (Quick Actions)
    if 'text_input' in request.form:
        transcript = request.form['text_input']
        print(f"DEBUG: Received Text Input: {transcript}")
    
    # Check for Audio input
    elif 'audio_data' in request.files:
        print("DEBUG: Audio File Received. Attempting Transcription...")
        audio_file = request.files['audio_data']
        
        # DEBUG: Check if Key exists
        if not deepgram_key:
            print("CRITICAL ERROR: Deepgram API Key is MISSING in .env file!")
        
        # Transcribe via Deepgram
        try:
            dg_resp = requests.post(
                DEEPGRAM_API_URL, 
                headers={"Authorization": f"Token {deepgram_key}", "Content-Type": "audio/*"},
                data=audio_file.read()
            )
            
            print(f"DEBUG: Deepgram Status Code: {dg_resp.status_code}")
            
            if dg_resp.status_code == 200:
                data = dg_resp.json()
                transcript = data['results']['channels'][0]['alternatives'][0]['transcript']
                print(f"DEBUG: Transcription Result: '{transcript}'")
            else:
                print(f"DEBUG: Deepgram Error Body: {dg_resp.text}")
                
        except Exception as e:
            print(f"DEBUG: Deepgram Exception: {e}")

    # Check for Vision input
    if 'image_data' in request.files:
        print("DEBUG: Image File Received.")
        image_file = request.files['image_data']
        image_bytes = image_file.read()
        image_part = {"mime_type": "image/jpeg", "data": image_bytes}

    # 2. MASTER AGENT ORCHESTRATION (Gemini)
    ai_text = ""
    active_agent = "agent-master"
    pdf_generated = False
    ueba_log = "UEBA: Monitoring session..."

    # LOGIC FIX: If transcript is empty, don't just say "I am listening".
    # Check if we have an image at least.
    if not transcript and not image_part:
        print("DEBUG: No Input Detected (Empty Transcript & No Image)")
        ai_text = "I am listening... Please speak closer to the mic."
    else:
        try:
            print("DEBUG: Sending to Gemini...")
            mock_data = get_mock_credit_score()
            
            sys_prompt = f"""
            You are the 'Tata Capital Master Agent'.
            USER INPUT: "{transcript}"
            CONTEXT: Customer: {mock_data['name']}, Credit Score: {mock_data['score']}
            
            AGENTS:
            1. 'agent-sales': General queries.
            2. 'agent-verify': IF image provided. Action: "ID Verified."
            3. 'agent-risk': Eligibility checks.
            4. 'agent-doc': "sanction", "letter".
            
            OUTPUT JSON ONLY: {{ "text": "...", "active_agent": "...", "ueba_log": "..." }}
            """
            
            model = genai.GenerativeModel('gemini-2.0-flash')
            content = [sys_prompt]
            if image_part: content.append(image_part)

            response = model.generate_content(content)
            print(f"DEBUG: Gemini Response: {response.text[:50]}...") # Print first 50 chars
            
            try:
                clean_json = response.text.replace("```json", "").replace("```", "").strip()
                res_data = json.loads(clean_json)
                ai_text = res_data.get("text")
                active_agent = res_data.get("active_agent")
                ueba_log = res_data.get("ueba_log", "UEBA: Action authorized.")
                
                if active_agent == "agent-doc":
                    generate_sanction_pdf(mock_data['limit'], mock_data['name'])
                    pdf_generated = True

            except Exception as e:
                print(f"DEBUG: JSON Parse Error: {e}")
                ai_text = response.text 
                
        except Exception as e:
            print(f"DEBUG: Gemini API Error: {e}")
            ai_text = "I am connecting to the secure server."

    # 3. VOICE SYNTHESIS
    audio_b64 = None
    if ai_text and len(ai_text) > 5: # Only generate audio if we have actual text
        try:
            print("DEBUG: Generating Voice...")
            payload = {"voiceId": "en-US-ken", "text": ai_text, "format": "MP3"}
            headers = {"Content-Type": "application/json", "api-key": murf_key}
            resp = requests.post(MURF_STREAM_URL, json=payload, headers=headers)
            if resp.status_code == 200:
                audio_b64 = base64.b64encode(resp.content).decode('utf-8')
            else:
                print(f"DEBUG: Murf Error {resp.status_code}")
        except: pass

    return jsonify({
        "user_text": transcript,
        "ai_text": ai_text,
        "audio_base64": audio_b64,
        "active_agent": active_agent,
        "ueba_log": ueba_log,
        "pdf_url": "/download_pdf" if pdf_generated else None
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)