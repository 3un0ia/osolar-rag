import json
import boto3
from config import BEDROCK_REGION, BEDROCK_MODEL, ANTHROPIC_VERSION, BEDROCK_MAX_TOKENS
from typing import Iterator

# 역할을 통해 자동으로 인증 정보를 가져옵니다.
_bedrock = boto3.client(
    "bedrock-runtime",
    region_name=BEDROCK_REGION
)

def _invoke_bedrock(prompt: str) -> Iterator[str]:
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
        accept = "text/event-steam",
        body = json.dumps(_body),
        stream=True
    )

    for event in resp["body"].iter_lines():
        if not event:
            continue
        data = json.loads(event.replace("data: ", ""))
        chunk = data["choices"][0]["delta"].get("content", "")
        yield chunk


def generate_response_stream(prompt: str) -> Iterator[str]:
    """
    스트리밍 응답을 위한 제너레이터 함수
    """
    yield from _invoke_bedrock(prompt)