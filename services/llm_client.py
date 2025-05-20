import json
import boto3
from config import BEDROCK_REGION, BEDROCK_MODEL, ANTHROPIC_VERSION, BEDROCK_MAX_TOKENS

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
        body = json.dumps(_body)
    )

    data = resp["body"].read().decode()
    return json.loads(data)["result"]

def generate_response(prompt: str) -> str:
    """
    외부(api/routes.py)에서 사용할 고수준 함수
    """
    return _invoke_bedrock(prompt)