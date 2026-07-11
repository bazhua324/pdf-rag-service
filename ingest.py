from dotenv import load_dotenv
from rag.pipeline import ingest_pdf
import sys

if __name__ == "__main__":
    load_dotenv()
    n = ingest_pdf(sys.argv[1])
    print(f"Ingested {n} chunks")