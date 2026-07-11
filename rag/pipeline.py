import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-2-preview")

def get_embedding():
    return GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

def ingest_pdf(pdf_path: str, persist_dir: str = CHROMA_DIR) -> int:
    docs = PyPDFLoader(pdf_path).load()
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = splitter.split_documents(docs)
    Chroma.from_documents(documents=splits,
                          embedding=get_embedding(),
                          persist_directory=persist_dir)
    return len(splits)