import os
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb.utils import embedding_functions

CORPUS_DIR = "data/corpus"
DB_DIR = "vector_store"

def get_stable_ef():
    return embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def build_database():
    print("--- Building Vector Database (Stable Mode) ---")
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_or_create_collection(name="support_knowledge", embedding_function=get_stable_ef())
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    
    for filename in os.listdir(CORPUS_DIR):
        if filename.endswith(".txt"):
            company_name = filename.split("_")[0].capitalize()
            with open(os.path.join(CORPUS_DIR, filename), 'r', encoding='utf-8') as f:
                chunks = text_splitter.split_text(f.read())
            
            for i, chunk in enumerate(chunks):
                collection.upsert(documents=[chunk], metadatas=[{"company": company_name}], ids=[f"{company_name}_{i}"])
            print(f"SUCCESS: Added {len(chunks)} chunks for {company_name}")
    print("--- Database Build Complete! ---")

def retrieve_context(query, company):
    """This was missing! It allows the AI to search the database."""
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection(name="support_knowledge", embedding_function=get_stable_ef())
    
    results = collection.query(
        query_texts=[query],
        n_results=3,
        where={"company": company.capitalize()} if company and company.lower() != 'none' else None
    )
    return "\n\n".join(results['documents'][0]) if results['documents'] else ""

if __name__ == "__main__":
    build_database()