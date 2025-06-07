from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from loaders.faq_loader    import load_faq_chunks
from loaders.pdf_loader    import load_policy_chunks
from config import EMBEDDING_MODEL, PERSIST_DIR

def ingest(collection_name: str, docs: list):
    embedder = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectordb = FAISS.from_documents(
        documents=docs,
        embedding=embedder
    )
    vectordb.save_local(PERSIST_DIR)
    
    print(f"[{collection_name}] ingested {len(docs)} docs")

if __name__ == "__main__":
    # ingest("faq",    load_faq_chunks())
    # ingest("policy", load_policy_chunks())
    faq_docs    = load_faq_chunks()
    policy_docs = load_policy_chunks()
    all_docs = faq_docs + policy_docs 
    print(f"[faq] {len(faq_docs)} docs")
    print(f"[policy] {len(policy_docs)} docs")

    ingest("documents", all_docs)