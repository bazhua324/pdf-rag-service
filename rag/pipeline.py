import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-2-preview")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash-lite")

PROMPT = ChatPromptTemplate.from_template(
    """
    Answer in a complete sentence and mention the supporting evidence from the context.
    If the answer is not in the context, say "I don't know"
    
    Context:
    {context}
    
    Question: 
    {question}
    
    Answer: 
    """

)

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

def ingest_pdf(pdf_path: str, persist_dir: str = CHROMA_DIR) -> int:
    docs = PyPDFLoader(pdf_path).load()
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = splitter.split_documents(docs)
    Chroma.from_documents(documents=splits,
                          embedding=get_embeddings(),
                          persist_directory=persist_dir)
    return len(splits)

class RAGPipeline:
    def __init__(self, persist_dir: str = CHROMA_DIR):
        self.vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=get_embeddings(),
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        self.llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0)

    def ask(self, question: str) -> dict:
        docs = self.retriever.invoke(question) # docs is the top-k retrieved CHUNKS
        context = "\n\n".join(d.page_content for d in docs)
        messages = PROMPT.format_messages(context=context, question=question)
        response = self.llm.invoke(messages)
        return {
            "answer": response.content,
            "sources": [
                {"page": d.metadata.get("page"),
                 "snippet": d.page_content[:200],}
                for d in docs
            ]
        }