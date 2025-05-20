from langchain.llms.base import LLM
from services.llm_client import generate_response

class BedrockLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "bedrock-claude3.5"

    def _call(self, prompt: str, stop=None) -> str:
        # 실제 Bedrock invoke_model을 래핑
        return generate_response(prompt)

    @property
    def _identifying_params(self):
        return {}