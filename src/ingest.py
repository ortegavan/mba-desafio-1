import os

from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():
    pdf_path = Path(PDF_PATH)
    if not pdf_path.is_absolute():
        pdf_path = Path(__file__).resolve().parent.parent / pdf_path

    docs = PyPDFLoader(str(pdf_path)).load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=False,
    )
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    )

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

    ids = [f"doc-{i}" for i in range(len(chunks))]
    store.add_documents(documents=chunks, ids=ids)

    print(
        f"Ingestão concluída: {len(chunks)} chunks armazenados na coleção "
        f"'{os.getenv('PG_VECTOR_COLLECTION_NAME')}'."
    )

if __name__ == "__main__":
    ingest_pdf()