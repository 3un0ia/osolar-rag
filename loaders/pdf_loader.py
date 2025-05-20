from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.schema import Document

PDF_DIR   = "data/policies"
CHUNK_SIZE = 400
CHUNK_OVER = 150

def load_policy_chunks(pdf_dir: str = PDF_DIR) -> list[Document]:
    splitter = TokenTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVER
    )
    all_docs: list[Document] = []

    for pdf_path in Path(pdf_dir).glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_path))
        # PDF의 모든 페이지를 Document 객체 리스트로 로드
        pages = loader.load()

        # 페이지 단위로든 전체 페이지 합친 후든, 청크 분할
        chunks = splitter.split_documents(pages)

        # 청크별로 metadata에 source(파일명) 추가
        for i, doc in enumerate(chunks):
            # 보장: metadata가 dict 형태여야 함
            meta = dict(doc.metadata or {})
            meta.update({
                "source_file": pdf_path.name,
                "chunk_index": i
            })
            # langchain.schema.Document은 immutable할 수 있으니 재생성
            all_docs.append(
                Document(
                    page_content=doc.page_content,
                    metadata=meta
                )
            )

    return all_docs