from typing import List, Dict, Tuple
from config import EMBEDDING_MODEL, CHROMA_PERSIST_DIR
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from services.bedrock_llm import BedrockLLM
from services.llm_client import generate_response


# 1) 임베딩 + 벡터스토어 + retriever
embedder = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
vectordb  = Chroma(
    persist_directory=CHROMA_PERSIST_DIR,
    embedding_function=embedder,
    collection_name="documents"
)

llm = BedrockLLM()

# 3) RetrievalQA 체인 생성
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectordb.as_retriever(search_kwargs={"k": 4}),
    return_source_documents=True,
)

def run_qa(
        question: str,
        user_info: Dict,
        history: List[str]
    ) -> Tuple[str, str]:

    docs = vectordb.similarity_search(question, k=4)

    context = "\n\n".join(d.page_content for d in docs)
    
    answer_prompt = build_answer_prompt(question, user_info, history, context)
    answer = generate_response(answer_prompt)

    summary_prompt = build_summary_prompt(question, user_info, history)
    summary = generate_response(summary_prompt)
    
    return answer, summary

def build_answer_prompt(
    question: str,
    user: Dict,
    history: List[str],
    contexts: List[str],
) -> str:
    hist_text = "\n".join(f"- {turn}" for turn in history)
    user_text = (
        f"사용자: {user.get('representativeName')} 님\n"
        f"발전소: {user.get('plantName')} (사업자번호 {user.get('businessNumber')})"
    )
    ctx_text = "\n\n".join(
        f"[문서 {i+1}]\n{ctx}" for i, ctx in enumerate(contexts)
    )

    return (
        f"{user_text}\n\n"
        f"대화 히스토리:\n{hist_text or '- 없음 -'}\n\n"
        f"관련 문서 조각 (contexts):\n{ctx_text}\n\n"
        f"질문: {question}\n\n"
        "위 정보를 종합하여, 정확하고 친절한 답변을 작성해 주세요."
    )


def build_summary_prompt(
    question: str,
    user: Dict,
    history: List[str],
) -> str:
    hist_text = "\n".join(f"- {turn}" for turn in history)
    return (
        "아래 사용자 정보와 대화 히스토리를 간략히 요약해 주세요.\n\n"
        f"사용자: {user.get('representativeName')} 님, 발전소: {user.get('plantName')}\n\n"
        f"대화 히스토리:\n{hist_text or '- 없음 -'}\n\n"
        f"요청 질문: {question}\n\n"
        "요약:"
    )