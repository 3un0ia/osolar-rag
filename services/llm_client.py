import json
import boto3
from config import BEDROCK_REGION, BEDROCK_MODEL, ANTHROPIC_VERSION, BEDROCK_MAX_TOKENS
from typing import Iterator

# 역할을 통해 자동으로 인증 정보를 가져옵니다.
_bedrock = boto3.client(
    "bedrock-runtime",
    region_name=BEDROCK_REGION
)

def _invoke_bedrock(prompt: str) -> str:
    # Claude 3.5 Sonnet용 Bedrock 호출
    _body = {
        "anthropic_version": ANTHROPIC_VERSION,
        "max_tokens": BEDROCK_MAX_TOKENS,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    resp = _bedrock.invoke_model(
        modelId = BEDROCK_MODEL,
        contentType = "application/json",
        accept = "application/json",
        # accept = "text/event-steam",
        body = json.dumps(_body),
    )

    # for event in resp["body"].iter_lines():
    #     if not event:
    #         continue
    #     data = json.loads(event.replace("data: ", ""))
    #     chunk = data["choices"][0]["delta"].get("content", "")
    #     yield chunk
    # 전체 응답을 문자열로 디코드하여 반환
    result = json.loads(resp["body"].read())
    return result["content"][0]["text"] if "content" in result else ""

def generate_response(prompt: str) -> str:
    yield from _invoke_bedrock(prompt)