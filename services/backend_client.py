import os
import requests
from config import BACKEND_BASE_URL, BACKEND_API_KEY, BACKEND_STREAM_URL



def fetch_user_profile(user_id: str) -> dict:
    """
    사내 백엔드의 /users/<user_id> 엔드포인트를 호출해
    사용자 프로필(예: 가입일, 등급, 과거 문의 이력 등)을 가져옵니다.
    """
    if not BACKEND_BASE_URL: return {}
    headers = {
    "Authorization": f"Bearer {BACKEND_API_KEY}"
    }
    url = f"{BACKEND_BASE_URL}/users/{user_id}"
    resp = requests.get(url, headers=headers, timeout=5)
    resp.raise_for_status()
    return resp.json()

def proxy_stream_to_backend(input_stream):
    """
    input_stream: request.environ['wsgi.input'] 처럼 파일-유사 객체
    """
    if not BACKEND_BASE_URL: return {}
    headers = {
        "Authorization": f"Bearer {BACKEND_API_KEY}",
        "Transfer-Encoding": "chunked",
    }
    # requests.post에 data로 제너레이터/스트림 파일 객체를 넘기면 chunked 전송
    resp = requests.post(
        BACKEND_STREAM_URL,
        data=input_stream,
        headers=headers,
        stream=True,   # 받는 쪽 응답도 스트리밍 처리 시
    )
    resp.raise_for_status()
    return resp