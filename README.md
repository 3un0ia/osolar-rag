# Osolar AI CS ChatBot

## 📖 프로젝트 개요

* LangChain 기반 RetrievalQA 파이프라인 사용
* 문서(FAQ, 정책 PDF)와 사용자 정보를 RAG 파이프라인으로 처리
* AWS Bedrock(Claude 3.5 Sonnet) + FAISS 벡터 스토어
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
├─ loaders/                # FAQ, PDF 로더
├─ scripts/                # 벡터 DB 데이터 주입 배치 스크립트 (ingest.py)
├─ service/
│  ├─ bedrock_llm.py       # Bedrock 호출 래퍼
│  ├─ llm_client.py        # LLM 응답 생성
│  └─ qa_chain.py          # LangChain RetrievalQA 체인
├─ app.py                  
├─ config.py               
└─ requirements.txt        
```


## 📡 API 사용 예

1. **문서 검색**

   ```bash
   curl -X POST http://localhost:8080/api/search_docs \
     -H "Content-Type: application/json" \
     -d '{"query":"<질의 내용>","top_k": <첨부할 관련 문서 개수>}'
   ```

2. **프롬프트 조립**

   ```bash
   curl -X POST http://localhost:8080/api/prompt \
     -H "Content-Type: application/json" \
     -d '{"docs":[{search_docs 응답(관련 문서 묶음)}], "user":{<사용자 정보 JSON>}, "question":"<질의 내용>?"}'
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
     -d '{"question":"<질의 내용>","user":{<사용자 정보 JSON>}}'
   ```


## 📄 라이선스

MIT License

> **Warning:**
> 실제 배포 전이나 aws access key 없이, Local server에서는 LLM 호출이 불가하며, EC2와 같은 AWS 서버 위에서는 동작 가능합니다.
> 또한 aws region이나 model에 대한 환경변수에 주의해 주세요.
