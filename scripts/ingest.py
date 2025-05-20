from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from loaders.faq_loader    import load_faq_chunks
from loaders.pdf_loader    import load_policy_chunks
from loaders.json_loader   import load_user_records
from config import EMBEDDING_MODEL

PERSIST_DIR        = "./chroma_persist"

def ingest(collection_name: str, docs: list):
    embedder = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embedder,
        persist_directory=PERSIST_DIR,
        collection_name=collection_name
    )
    
    print(f"[{collection_name}] ingested {len(docs)} docs")

if __name__ == "__main__":
    # ingest("faq",    load_faq_chunks())
    # ingest("policy", load_policy_chunks())
    # ingest("users",  load_user_records())
    faq_docs    = load_faq_chunks()
    policy_docs = load_policy_chunks()
    # user_docs   = load_user_records()
    all_docs = faq_docs + policy_docs # + user_docs
    print(f"[faq] {len(faq_docs)} docs")
    print(f"[policy] {len(policy_docs)} docs")
    # print(f"[user] {len(user_docs)} docs")

    ingest("documents", all_docs)