from config import EMBEDDING_MODEL, CHROMA_PERSIST_DIR
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from services.bedrock_llm import BedrockLLM
from services.llm_client import generate_response

template = """
You are an AI assistant with deep knowledge of company FAQ and internal policies.
Use the following context to answer the user’s question as accurately and concisely as possible.

Context:
{context}

User Profile:
{user_profile}

Question:
{question}

Answer:
""".strip()

# 1) 임베딩 + 벡터스토어 + retriever
embedder = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
vectordb  = Chroma(
    persist_directory=CHROMA_PERSIST_DIR,
    embedding_function=embedder,
    collection_name="documents"
)

llm = BedrockLLM()

# 3) RetrievalQA 체인 생성
qa    = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectordb.as_retriever(search_kwargs={"k": 4}),
    return_source_documents=True,
)

def run_qa(
        question: str,
        user_profile: dict = None,
        top_k: int = 4,
        skip_llm: bool = False
    ) :
    docs = vectordb.similarity_search(question, k=top_k)

    context = "\n\n".join(d.page_content for d in docs)
    prompt = template.format(
        context=context,
        question=question,
        user_profile=user_profile or {}
    )
    
    answer = None if skip_llm else generate_response(prompt)
    
    return {
        "prompt": prompt,
        "answer": answer,
        "documents": [
            {
                "id": d.metadata.get("id"),
                "score": getattr(d, "score", None),
                **d.metadata
            }
            for d in docs
        ]
    }