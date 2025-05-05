from flask import Flask, render_template, request
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer, util
from spellchecker import SpellChecker
from flask import Flask, render_template, request, jsonify
import smtplib
from email.message import EmailMessage
from flask import jsonify
import smtplib
from email.mime.text import MIMEText
import torch
import json
import pickle
import random
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")  # or directly set your API key string

def generate_ai_journal_prompt(user_entry):
    prompt = (
        f"You are a journaling assistant helping users reflect on their feelings. "
        f"The user wrote: '{user_entry}'. "
        f"Ask one gentle follow-up question to help them explore their thoughts further."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.7,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print(f"AI journaling error: {e}")
        return "I'm here for you. Could you tell me more about what you're feeling?"


# === Initialize Flask ===
app = Flask(__name__)
app.static_folder = 'static'

# === Load Classifier Model & Tokenizer ===
model_path = "model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# === Load Training Tags ===
with open("labels.pkl", "rb") as f:
    tags = pickle.load(f)

# === Load Intents ===
with open("intents_filtered.json", "r") as f:
    filtered_intents = json.load(f)

intent_responses = {intent["tag"]: intent["responses"] for intent in filtered_intents["intents"]}

# === Load Sentence Transformer for Semantic Similarity ===
model_sbert = SentenceTransformer('all-MiniLM-L6-v2')

# === Profanity & Spellcheck ===
spell = SpellChecker()
BAD_WORDS = {"damn", "suck", "asshole", "bastard", "fuck", "shit", "crap", "bitch"}

def correct_spelling(text):
    return " ".join([spell.correction(word) if word.lower() in spell.unknown([word]) else word for word in text.split()])

def contains_bad_words(text):
    return any(word.lower() in BAD_WORDS for word in text.split())

# === Prepare Pattern Embeddings ===
pattern_map = []
for intent in filtered_intents["intents"]:
    tag = intent["tag"]
    for pattern in intent["patterns"]:
        emb = model_sbert.encode(pattern, convert_to_tensor=True)
        pattern_map.append({"embedding": emb, "tag": tag})

# === Predict Intent Using Semantic Similarity ===
def predict_intent_semantic(user_input, threshold=0.65):
    input_emb = model_sbert.encode(user_input, convert_to_tensor=True)
    scores = [(util.pytorch_cos_sim(input_emb, p["embedding"]).item(), p["tag"]) for p in pattern_map]
    best_score, best_tag = max(scores, key=lambda x: x[0])
    print(f"[DEBUG] Semantic Score: {best_score:.2f} — Tag: {best_tag}")
    return best_tag if best_score >= threshold else None

# === Fallback Classifier ===
def predict_intent_classifier(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    predicted_index = torch.argmax(outputs.logits).item()
    return tags[predicted_index]

# === Get Response ===
def get_response(intent):
    return random.choice(intent_responses.get(intent, ["Sorry, I didn't understand that."]))

# === Guided Journaling ===
def save_journal_entry(entry):
    os.makedirs("journals", exist_ok=True)
    with open("journals/user_journal.txt", "a", encoding="utf-8") as f:
        f.write(entry + "\n")

# === Routes ===
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/meditate")
def meditate():
    return render_template("meditation.html")

@app.route("/get")
def get_bot_response():
    raw_input = request.args.get("msg")
    if contains_bad_words(raw_input):
        return "Let's keep things respectful. I'm here to help you feel better."

    user_input = correct_spelling(raw_input)
    intent = predict_intent_semantic(user_input)
    if not intent:
        intent = predict_intent_classifier(user_input)

    print(f"[DEBUG] User: {user_input} → Intent: {intent}")

    if intent == "journal-start":
        return "Sure! Here's your journaling space. [JOURNAL_BTN]"

    response = get_response(intent)

    #Meditation trigger
    if intent in ["anxious", "stressed", "i am feeling anxious lately.", "i am stressed out", "meditation"]:
        response += " [MEDITATE_BTN]"

    # Journaling trigger
    if intent in ["journal", "journal-entry", "i want to journal"]:
        response += " [JOURNAL_BTN]"
    return response

@app.route("/journal")
def journal():
    user_entry = request.args.get("entry", "")
    ai_prompt = generate_ai_journal_prompt(user_entry)
    return render_template("journal.html", prompt=ai_prompt)

@app.route("/suggest_journal")
def suggest_journal():
    suggestions = [
        "What made you smile today?",
        "What is something you'd like to let go of?",
        "Write down 3 things you're grateful for.",
        "Describe a moment when you felt proud recently.", 
        "Describe everything you did today. Were there any instances throughout the day that made you feel differently?"
    ]
    return random.choice(suggestions)

@app.route("/email_journal", methods=["POST"])
def email_journal():
    data = request.get_json()
    entry = data.get("entry")
    if not entry:
        return "No journal content found.", 400

    # Replace with your email setup
    try:
        msg = EmailMessage()
        msg.set_content(entry)
        msg['Subject'] = "Your Journal Entry from Siri Bot"
        msg['From'] = "your_email@example.com"
        msg['To'] = "user_email@example.com"  # Replace with dynamic email if available

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login("your_email@example.com", "your_app_password")
            smtp.send_message(msg)

        return "Your journal entry has been emailed successfully."
    except Exception as e:
        print(e)
        return "Failed to send email.", 500

def email_journal():
    data = request.get_json()
    user_email = data["email"]
    journal_entry = data["entry"]

    # Replace these with your actual email credentials (or setup SMTP securely)
    sender_email = "sirihegde02@gmail.com"
    sender_password = "pgjo quyq dfdj qqne"

    try:
        msg = MIMEText(journal_entry)
        msg["Subject"] = "Your Journal Entry"
        msg["From"] = sender_email
        msg["To"] = user_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, user_email, msg.as_string())

        return "Email sent successfully!"
    except Exception as e:
        print(f"[ERROR] {e}")
        return "Failed to send email.", 500

# === Start App ===
if __name__ == "__main__":
    app.run(debug=True)
