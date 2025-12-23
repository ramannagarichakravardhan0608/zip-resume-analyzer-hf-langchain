# 📦 ZIP Resume Analyzer (Hugging Face + LangChain)

A professional AI-powered resume analysis application built with **Streamlit**, **LangChain**, and **Hugging Face LLMs**.  
This tool allows users to upload a ZIP file containing multiple resumes (PDF/DOCX) and automatically extracts structured information such as name, email, skills, and professional summary.

---

## 🚀 Features

- Upload a ZIP file containing multiple resumes
- Supports **PDF** and **DOCX** formats
- Uses **Mistral-7B-Instruct** via Hugging Face
- Structured data extraction using **PydanticOutputParser**
- Clean and interactive **Streamlit UI**
- Fully local ZIP extraction and processing

---

## 🧠 Tech Stack

- **Python**
- **Streamlit**
- **LangChain**
- **Hugging Face Inference API**
- **Mistral-7B-Instruct**
- **Pydantic**
- **PyPDF**
- **python-docx**

---
🔑 Environment Setup

Create a .env file in the root directory:
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here

📦 Installation
git clone https://github.com/your-username/zip-resume-analyzer-hf-langchain.git
cd zip-resume-analyzer-hf-langchain
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

▶️ Run the Application
streamlit run main.py


📝 How It Works

User uploads a ZIP file containing resumes

ZIP is extracted locally

Each PDF/DOCX resume is read and converted to text

LangChain sends resume text to Hugging Face LLM

Structured data is extracted using Pydantic schema

Output is displayed in clean JSON format

📌 Sample Output
{
  "name": "John Doe",
  "email": "john.doe@email.com",
  "skills": ["Python", "Machine Learning", "SQL"],
  "summary": "Data analyst with 3+ years of experience..."
}

👨‍💻 Author

Chakravardhan
Machine Learning & Generative AI Enthusiast




