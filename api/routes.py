import json
from flask import Response, stream_with_context
from flask import Blueprint, request, jsonify
from services.qa_chain import run_qa, vectordb, build_answer_prompt
from services.llm_client import generate_response
import re
CONTROL_CHAR_RE = re.compile(r'[\x00-\x1F]+')

bp = Blueprint("api", __name__)

@bp.route("/query", methods=["POST"])
def query_stream():
    body = request.get_json()
    errors = []

    if body is None:
        errors.append({
            "loc": ["body"],
            "msg": "Invalid or missing JSON body",
            "type": "value_error.json"
        })
        return jsonify(detail=errors), 422
    
    question = body.get("question","")
    user_info = body.get("user", {})
    history = body.get("history", [])

    if not question :
        errors.append({
            "loc": ["body", "question"],
            "msg": "Field required and must be a non-empty string",
            "type": "value_error.missing"
        })
    if history is None or not isinstance(history, list):
        errors.append({
            "loc": ["body", "history"],
            "msg": "If provided, history must be a list of strings",
            "type": "type_error.list"
        })

    if errors:
        return jsonify(detail=errors), 422
    
    # generator = run_qa(question, user_info, history)
    # def event_stream():
    #     for chunk in generator:
    #         yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"

    answer, summary = run_qa(question, user_info, history)
    
    if hasattr(answer, '__iter__') and not isinstance(answer, str):
        answer = "".join(answer)
    if hasattr(summary, '__iter__') and not isinstance(summary, str):
        summary = "".join(summary)
    
    body = json.dumps({
        "answer": answer,
        "summary": summary
    }, ensure_ascii=False)

    return Response(body, content_type="application/json; charset=utf-8")

    # return Response(
    #     stream_with_context(event_stream()),
    #     mimetype="text/event-stream; charset=utf-8"
    #     )

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
            "score":        float(score),
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
    user_profile = data.get("user", {})
    history      = data.get("history", [])

    # Context 조립: front-end에서 보내준 docs 리스트를 그대로 사용
    context = "\n\n".join(d.get("page_content", "") for d in docs)

    # LangChain PromptTemplate 에 입력 변수로 넘겨서 문자열 생성
    answer_prompt = build_answer_prompt(question, user_profile, history, context)
    # answer = generate_response(answer_prompt)
    body = json.dumps(
        {"prompt": answer_prompt},
        ensure_ascii=False,
        indent=2,
        )
    
    return Response(body, content_type="application/json; charset=utf-8")