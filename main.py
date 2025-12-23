import os
import zipfile
import tempfile
from typing import List

import streamlit as st
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from pydantic import BaseModel, Field
from pypdf import PdfReader
from docx import Document


load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if not HF_TOKEN:
    st.error("Hugging Face API key not found in .env")
    st.stop()

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    task="conversational",
    huggingfacehub_api_token=HF_TOKEN,
    temperature=0,
    max_new_tokens=512,
)

chat_model = ChatHuggingFace(llm=llm)


class ResumeSchema(BaseModel):
    name: str = Field(description="Candidate full name")
    email: str = Field(description="Email address")
    skills: List[str] = Field(description="List of technical skills")
    summary: str = Field(description="Short professional summary")

parser = PydanticOutputParser(pydantic_object=ResumeSchema)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a professional resume analyzer. Extract structured data exactly in the requested format."
        ),
        (
            "human",
            """
{format_instructions}

Resume Text:
{text}
"""
        )
    ]
)

def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def read_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

st.set_page_config(page_title="ZIP Resume Analyzer (HF)", layout="centered")
st.title("📦 ZIP Resume Analyzer (Hugging Face + LangChain)")

zip_file = st.file_uploader(
    "Upload ZIP file containing PDF/DOCX resumes",
    type=["zip"]
)

if zip_file and st.button("Analyze Resumes"):
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, zip_file.name)

        with open(zip_path, "wb") as f:
            f.write(zip_file.read())

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(tmpdir)

        chain = prompt | chat_model | parser

        for filename in os.listdir(tmpdir):
            file_path = os.path.join(tmpdir, filename)

            if filename.lower().endswith(".pdf"):
                text = read_pdf(file_path)
            elif filename.lower().endswith(".docx"):
                text = read_docx(file_path)
            else:
                continue

            try:
                result = chain.invoke({
                    "text": text,
                    "format_instructions": parser.get_format_instructions()
                })

                st.subheader(f"📄 {filename}")
                st.json(result.dict())

            except Exception as e:
                st.error(f"Failed to parse {filename}")
                st.write(e)
