# 🧠 Siri the Psychologist — AI Mental Health Chatbot

Welcome to **Siri the Psychologist**, an AI-powered mental health chatbot designed to provide a safe, supportive space for users to express their thoughts, practice mindfulness, and reflect through guided journaling.

This project includes:
- 💬 A personalized chatbot using NLP and semantic intent matching
- 🧘 A calming **guided meditation** screen with breathing animations and music
- ✍️ An AI-assisted **journaling interface** with email export
- 🤖 Spell correction, profanity filtering, and emotionally aware responses

---

## 🌟 Features

- **Chatbot** powered by `SentenceTransformer` + DistilBERT classifier  
- **Guided Meditation** with relaxing music and animated box breathing  
- **AI Journaling Assistant** that helps users reflect and email their entries  
- **Spelling correction** using `pyspellchecker`  
- **Profanity filter** to keep interactions respectful  
- **Responsive UI** with clean, calming visuals

---

## 🛠 Tech Stack

- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Python, Flask  
- **NLP**: `transformers`, `sentence-transformers`, `torch`  
- **Other tools**: Git LFS, jQuery, OpenAI API, Email via SMTP

---

## 🚀 Run It Locally

```bash
git clone https://github.com/Sirihegde02/Mental-health-Chatbot-1.git
cd Mental-health-Chatbot-1

# Install dependencies
pip install -r requirements.txt

# Run Flask server
flask --app app --debug run
