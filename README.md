# AI-Intelligence-System
An LLM-powered recruitment and resume optimization platform built during a **State-Level Hackathon**. This application features a dual-mode interface designed to assist both job seekers and HR managers.

## 🚀 Key Features

* **Job Seeker Mode (ATS Optimization):** Parses PDF resumes to calculate an accurate ATS match score and provides actionable suggestions to fix keyword gaps and formatting issues.
* **HR Manager Mode (Skill Screening):** Allows recruiters to input target skill sets, automatically evaluates how well a candidate's profile aligns with those requirements, and delivers a structured hiring verdict.

## 🛠️ Tech Stack

* **LLM Engine:** Groq API
* **Frontend UI:** Streamlit
* **Document Parser:** pdfplumber
* **Language:** Python

## 📁 Project Structure

```text
├── code/
│   ├── app1.py           # Streamlit Frontend UI
│   ├── llm_engine.py     # Groq API Integration & Prompts
│   ├── pdf_parser.py     # Text Extraction Logic
│   └── utils.py          # Helper Functions
├── requirements.txt      # Project Dependencies
└── README.md             # Project Documentation
