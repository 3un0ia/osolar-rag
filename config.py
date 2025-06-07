# BEDROCK_ENDPOINT, BEDROCK_MODEL, CHROMA_URL 등
from dotenv import load_dotenv
import os

load_dotenv()

# AWS Bedrock 접속 정보
BEDROCK_REGION = "us-east-1"
BEDROCK_MODEL  = "anthropic.claude-3-5-sonnet-20240620-v1:0"
ANTHROPIC_VERSION    = "bedrock-2023-05-31"
BEDROCK_MAX_TOKENS   = 1000
PERSIST_DIR = "./faiss_persist"

EMBEDDING_MODEL = "snunlp/KR-SBERT-V40K-klueNLI-augSTS"  
QUALITY_THRESHOLD = 0.8                # LLM 응답 재생성 기준