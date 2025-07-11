import json
from typing import Iterator, List, Dict, Tuple
from config import EMBEDDING_MODEL, PERSIST_DIR
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from services.bedrock_llm import BedrockLLM
from services.llm_client import generate_response

embedder = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
vectordb = FAISS.load_local(
    PERSIST_DIR,
    embedder,
    allow_dangerous_deserialization=True
)
llm = BedrockLLM()
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectordb.as_retriever(search_kwargs={"k": 4}),
    return_source_documents=True,
)


# def run_qa_stream(
#         question: str,
#         user_info: Dict,
#         history: List[str]
#     ) -> Iterator[Dict[str, str]]:
    
#     docs = vectordb.similarity_search(question, k=4)
#     context = "\n\n".join(d.page_content for d in docs)
    
#     answer_prompt = build_answer_prompt(question, user_info, history, context)
#     for chunk in generate_response(answer_prompt):
#         yield {"type": "answer", "text": chunk}
    
#     summary_prompt = build_summary_prompt(answer_prompt)
#     for chunk in generate_response(summary_prompt):
#         yield {"type": "summary", "text": chunk}


def run_qa(
        question: str,
        user_info: Dict,
        history: List[str]
    ) -> Tuple[str, str]:

    docs = vectordb.similarity_search(question, k=4)

    context = "\n\n".join(d.page_content for d in docs)
    
    answer_prompt = build_answer_prompt(question, user_info, history, context)
    answer = generate_response(answer_prompt)

    if isinstance(answer, (list, Iterator)):
        answer = "".join(str(chunk) for chunk in answer)
    elif isinstance(answer, dict):
        answer = json.dumps(answer, ensure_ascii=False)

    summary_prompt = build_summary_prompt(answer)
    summary = generate_response(summary_prompt)
    
    return answer, summary

def build_answer_prompt(
    question: str,
    user: Dict,
    history: List[str],
    context: str,
) -> str:
    if history:
        hist_text = "\n".join(f"{i+1}. {turn}" for i, turn in enumerate(history))
    else:
        hist_text = "이전 대화 이력 없음"
    user_text = json.dumps(user, ensure_ascii=False, indent=2)
    ctx_text = context

    return (
        "당신은 osolar CS 챗봇입니다. 서비스와 관련되지 않은 질문에는 응답 불가함을 명시해주세요.\n\n"
        "아래 정보를 바탕으로 질문에 대한 답변을 작성해 주세요.\n\n"
        f"== 사용자 정보 ==\n"
        f"{user_text}\n\n"
        f"== 이전 대화 이력 ==\n"
        f"{hist_text}\n\n"
        f"== 관련 문서 컨텍스트 ==\n"
        f"{ctx_text}\n\n"
        f"== 현재 질문 ==\n"
        f"{question}\n\n"
        "위 정보를 종합하여, 정확하고 친절한 답변을 작성해 주세요."
    )


def build_summary_prompt(
    answer: str
) -> str:
    return (
        "아래 응답을 한 문장으로 요약해 주세요:\n\n"
        f"{answer}\n\n"
        "요약:"
    )