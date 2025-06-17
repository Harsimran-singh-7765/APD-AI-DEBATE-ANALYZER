# 🧠 APD-AI-DEBATE-ANALYZER

An AI-powered debate analysis tool that simulates a **National-Level Adjudicator** for **Asian Parliamentary Debate (APD)**.

This tool helps analyze 6 speeches from an APD round and provides:

- 📋 **Detailed adjudication**
- 💬 **Constructive feedback**
- 🏆 **Final verdict with best speaker selection**

---

## 🎯 Features

- 🎙️ **Upload or record 6 speeches**:  
  - PM, DPM, and Government Whip  
  - LO, DLO, and Opposition Whip  

- 🔁 **Auto Transcription**:  
  - Transcribes audio to text using **OpenAI Whisper**

- 🧠 **AI-Powered Judgement**:  
  - Uses **CrewAI Agents** and **Gemini API** to simulate a professional adjudicator

- ✅ **Test Case Included**:  
  - Toggle demo mode to test without audio files

---

## 🗂 File Structure

📁 APD-AI-DEBATE-ANALYZER/
├── APD.py # Streamlit web app file
├── requirements.txt # Python libraries required
└── README.md # Project overview and setup instructions



---

## 🚀 How to Run Locally

> Clone the repository and launch the Streamlit app:

```bash
git clone https://github.com/Harsimran-singh-7765/APD-AI-DEBATE-ANALYZER.git
cd APD-AI-DEBATE-ANALYZER
pip install -r requirements.txt
streamlit run APD.py
```

## 🧪 Demo Mode (No Recordings Required)
The app includes a demo toggle that lets you test everything instantly using 6 preloaded sample speeches. Great for debugging or fast demos!

## 🧠 How it Works
Upload or record 6 speeches

Whisper transcribes audio to text

Each speaker's transcript is passed to a CrewAI Agent

A Judge Agent then:

Analyzes speaker roles, clash quality, and rebuttals

Provides constructive feedback

Declares a winner

Ranks all 6 speakers

Identifies the best speaker

## 🧪 Technologies Used
Streamlit

CrewAI

Google Gemini API

OpenAI Whisper

## 🙌 Credits
Made with ❤️ by Harsimran Singh
Built to assist debaters, judges, and APD learners with fair and insightful AI analysis.

## 📌 Note
Make sure to set your GEMINI_API_KEY inside a .env file or Streamlit secret manager.

If deploying online (e.g., Streamlit Cloud), make sure to follow the deployment-specific instructions to handle SQLite/Chroma errors.
