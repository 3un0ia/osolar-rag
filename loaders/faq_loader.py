from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.schema import Document

FAQ_PATH = "data/FAQs.txt"

def load_faq_chunks(chunk_size: int = 400, chunk_overlap: int = 150) -> list[Document]:
    # 1) TextLoader로 로드
    loader = TextLoader(FAQ_PATH, encoding="utf-8")
    docs   = loader.load()

    # 2) LangChain splitter로 청크 분할
    splitter = TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(docs)