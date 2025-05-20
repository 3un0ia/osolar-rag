rag/
├─ data/                     # 원본 데이터 보관
│  ├─ faq/                   # FAQ 텍스트 파일들
│  │   └─ faq.txt
│  ├─ policy/                # 태양광 정책 PDF들
│  │   └─ solar_policy.pdf
│  └─ users.json             # 서비스 사용자 JSON 데이터
│
├─ loaders/                  # 로더: raw data → 텍스트 청크
│  ├─ faq_loader.py          # faq.txt 파싱 및 청크 분할
│  ├─ pdf_loader.py          # PDF → 텍스트 추출, 청크 분할
│  └─ json_loader.py         # users.json 읽고 검증 → 딕셔너리 리스트
│
├─ embeddings/               # 임베딩 생성 및 캐싱
│  ├─ embedder.py            # AWS Bedrock 호출: Claude 3.5 Sonnet 임베딩 API 래퍼
│  └─ batch_embed.py         # 대량 텍스트를 배치 처리/로컬 캐시 관리
│
├─ vectorstore/              # 벡터 DB 연동
│  ├─ chroma_client.py       # ChromaDB 커넥션 & 컬렉션 관리
│  └─ store.py               # “문서-ID ↔ 벡터” 저장/조회 유틸
│
├─ search/                   # 키워드 추출 & 유사도 검색
│  ├─ keyword_extractor.py   # 질의 임베딩 → 키워드 후보 벡터 매핑
│  └─ similarity_search.py   # (keyword, similarity) 튜플 리스트 반환
│
├─ scripts/                  # 일회성/배치 스크립트
│  ├─ ingest_faq.py          # FAQ → 임베딩 → 벡터 DB 적재
│  ├─ ingest_policy.py       # PDF 정책문서 적재
│  └─ ingest_users.py        # 사용자 JSON 적재
│
├─ config.py                 # 환경변수(BEDROCK_ENDPOINT, BEDROCK_MODEL, CHROMA_URL 등)
├─ requirements.txt          # 의존 패키지 목록(`boto3`, `chromadb`, `langchain` 등)
└─ README.md                 # 프로젝트 개요·설치·사용법