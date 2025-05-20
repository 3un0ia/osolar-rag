import json
from flask import Response
from flask import Blueprint, request, jsonify
from services.qa_chain import run_qa, vectordb, template
from services.llm_client import generate_response
import services.backend_client as backend_client
import re
CONTROL_CHAR_RE = re.compile(r'[\x00-\x1F]+')

bp = Blueprint("api", __name__)

@bp.route("/query", methods=["POST"])
def query():
    data = request.get_json()

    question = data.get("question","")
    top_k = data.get("top_k", 5)
    skip_llm = data.get("skip_llm", False)

    # 1) 검색
    answer, docs = run_qa(question)
    # # 2) 프롬프트
    # context = "\n\n".join(doc.page_content for doc, _ in docs_scores)
    # prompt  = template.format(
    #             context=context, 
    #             question=question, 
    #             user_profile=user_profile
    #     )
    # 3) LLM 호출
    if skip_llm:
        answer = None

    # 4) 결과 반환
    return jsonify({
        "answer": answer,
        "documents": [
            {
                "id": d.metadata.get("id"), 
                "score": getattr(d, "score", None)
            }
            for d in docs
        ]
    })

@bp.route("/search_docs", methods=["POST"])
def search_docs():
    data    = request.get_json()

    query   = data.get("query", "")
    top_k   = data.get("top_k", 5)

    docs_scores = vectordb.similarity_search_with_score(query, k=top_k)
    
    out = []

    import re
    CONTROL_CHAR_RE = re.compile(r'[\x00-\x1F]+')

    for doc, score in docs_scores:
        text = CONTROL_CHAR_RE.sub('', doc.page_content)
        out.append({
            "id":           doc.metadata.get("id"),
            "score":        score,
            "metadata":     doc.metadata,
            "page_content": text
        })

    payload = out

    body = json.dumps(payload, ensure_ascii=False)
    return Response(body, content_type="application/json; charset=utf-8")



@bp.route("/prompt", methods=["POST"])
def prompt():
    data         = request.get_json() or {}

    docs         = data.get("documents", [])
    question     = data.get("question", "")
    user_profile = data.get("user_profile", {})

    # Context 조립: front-end에서 보내준 docs 리스트를 그대로 사용
    context = "\n\n".join(d.get("page_content", "") for d in docs)

    # LangChain PromptTemplate 에 입력 변수로 넘겨서 문자열 생성
    prompt_str = template.format(
        context=context,
        question=question,
        user_profile=user_profile
    )
    return jsonify({"prompt": prompt_str})


@bp.route("/llm", methods=["POST"])
def llm_only():
    data   = request.get_json() or {}
    prompt = data.get("prompt", "")

    # Bedrock 호출
    try:
        answer = generate_response(prompt)
    except Exception as e:
        print("🔴 LLM 호출 오류:", e)
        return jsonify({"error": str(e)}), 400
    return jsonify({"response": answer})