import json
from langchain.schema import Document

USER_JSON_PATH = "data/users.json"

def load_user_records() -> list[Document]:
    with open(USER_JSON_PATH, "r", encoding="utf-8") as f:
        users = json.load(f)

    docs = []
    for u in users:
        if "id" not in u:
            raise ValueError("User record missing 'id'")
        # JSON 전체를 하나의 문서로 취급
        docs.append(
            Document(
                page_content=json.dumps(u, ensure_ascii=False),
                metadata=u
            )
        )
    return docs