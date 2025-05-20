# Osola AI 서비스

## 📖 프로젝트 개요

* LangChain 기반 RetrievalQA 파이프라인 사용
* 문서(FAQ, 정책 PDF)와 사용자 정보를 RAG 파이프라인으로 처리
* AWS Bedrock(Claude 3.5 Sonnet) + ChromaDB 벡터 스토어
* Flask 기반 REST API(키워드 추출 → 문서 검색 → 프롬프트 생성 → LLM 호출 → 응답 반환)

## 🚀 주요 기능

1. **질의 키워드 추출**
2. **벡터 유사도 검색** (`/api/search_docs`)
3. **프롬프트 조립** (`/api/prompt`)
4. **LLM 응답 생성** (`/api/llm`)
5. **최종 QA 흐름** (`/api/query`)

## 🏗️ 아키텍처

```
[Client] → Flask(API) → (1) KeywordExtractor
                         → (2) VectorStore(ChromaDB)
                         → (3) PromptGenerator
                         → (4) LLMClient(Bedrock)
                         → [Client]
```

## 📁 디렉토리 구조

```
.
├─ api/
│  └─ routes.py            # 엔드포인트 정의
├─ data/                   # 정책 문서 및 사용자 정보
├─ loaders/                # FAQ, PDF, JSON 로더
├─ scripts/                # 벡터 DB 데이터 주입 배치 스크립트 (ingest.py)
├─ service/
│  ├─ backend_client.py    # 백엔드 서버 통신
│  ├─ bedrock_llm.py       # Bedrock 호출 래퍼
│  ├─ llm_client.py        # LLM 재시도·에러 핸들링
│  └─ qa_chain.py          # LangChain RetrievalQA 체인
├─ app.py                  
├─ config.py               
└─ requirements.txt        
```

## 📋 설치 및 실행

1. **클론 & 가상환경 생성**

   ```bash
   git clone <your-repo-url>
   cd <repo>
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **의존성 설치**

   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```

3. **ChromaDB 서버(로컬)**

   ```bash
   docker run -d -p 8000:8000 ghcr.io/chroma-core/chroma:latest
   ```

4. **데이터 적재**

   ```bash
   python scripts/ingest.py
   # 또는
   python -m scripts/ingest
   ```

5. **Flask 서버 실행**

   ```bash
   export FLASK_ENV=development
   export PORT=8080
   python app.py
   # 또는
   gunicorn app:app --bind 0.0.0.0:8080
   ```

## 🔧 환경 변수 (`.env` 또는 export)

```dotenv
BEDROCK_REGION=us-east-1
BEDROCK_MODEL=anthropic.claude-3-5-sonnet-20240620-v1:0
CHROMA_PERSIST_DIR=./chroma_persist
PORT=8080
```

## 📡 API 사용 예

1. **문서 검색**

   ```bash
   curl -X POST http://localhost:8080/api/search_docs \
     -H "Content-Type: application/json" \
     -d '{"query":"오솔라 서비스 가입은 어떻게 하나요?","top_k":3}'
   ```

2. **프롬프트 조립**

   ```bash
   curl -X POST http://localhost:8080/api/prompt \
     -H "Content-Type: application/json" \
     -d '{"docs":[{…}], "user":{}, "question":"오솔라 서비스 가입은 어떻게 하나요?"}'
   ```

3. **LLM 호출**

   ```bash
   curl -X POST http://localhost:8080/api/llm \
     -H "Content-Type: application/json" \
     -d '{"prompt":"<프롬프트 문자열>"}'
   ```

4. **전체 QA 플로우**

   ```bash
   curl -X POST http://localhost:8080/api/query \
     -H "Content-Type: application/json" \
     -d '{"question":"오솔라 서비스 가입은 어떻게 하나요?","user_id":"USER123"}'
   ```

## 🧪 테스트

* 로컬에서 `curl` 또는 Postman으로 각 엔드포인트 동작 확인
* `pytest` 등 테스트 스크립트 추가 가능

## ☁️ 배포 가이드 (EC2)

1. EC2에 SSH/SSM 접속 → 코드 배포
2. IAM 인스턴스 프로파일에 Bedrock 권한 부여
3. `venv` 재생성 → `pip install` → `gunicorn app:app`
4. 보안 그룹에 8080 포트 열기
5. (Optional) Nginx → `/api/*` 리버스 프록시

## ⚙️ 트러블슈팅

* **ChromaDB 연결 오류** → `rm -rf ./chroma_persist` 후 재ingest
* **Bedrock 권한 에러** → `aws sts get-caller-identity` 로 인스턴스 프로파일 확인
* **429 RateLimit** → `top_k` 또는 `max_tokens` 조정, 테스트 시 OpenAI로 대체

## 🤝 기여

1. Fork → branch 생성
2. PR → 코드 리뷰 → Merge

## 📄 라이선스

MIT License

> **Tip:** 실제 배포 전에는 `requirements.txt` 를 반드시 `pip freeze` 로 최신화하고, 불필요한 개발 의존성은 제거하세요.
