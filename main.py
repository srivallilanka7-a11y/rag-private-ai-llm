from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse
from rag import store_pdf_text, retrieve_context
from pypdf import PdfReader
from langchain_openai import ChatOpenAI
import os
from langchain_openai import ChatOpenAI
app = FastAPI()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)


@app.get("/", response_class=HTMLResponse)
def home():
    with open("frontend.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/upload")
async def upload_pdf(file: UploadFile):
    reader = PdfReader(file.file)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    store_pdf_text(text)
    return {"message": "PDF processed successfully"}

@app.post("/ask")
async def ask(question: str = Form(...)):
    context = retrieve_context(question)

    response = llm.invoke(
        f"Answer only from this context:\n{context}\n\nQuestion: {question}"
    )

    return {"answer": response.content}