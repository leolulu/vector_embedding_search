from langchain.embeddings import OpenAIEmbeddings


class OpenAIEmbeddingEngine:
    EMBEDDING_ENGINE: OpenAIEmbeddings

    @staticmethod
    def _init_engine():
        if 'EMBEDDING_ENGINE' not in OpenAIEmbeddingEngine.__dict__:
            OpenAIEmbeddingEngine.EMBEDDING_ENGINE = OpenAIEmbeddings()  # type: ignore

    @staticmethod
    def embed_document(text) -> list[float]:
        OpenAIEmbeddingEngine._init_engine()
        doc_result = OpenAIEmbeddingEngine.EMBEDDING_ENGINE.embed_documents([text])
        return doc_result[0]

    @staticmethod
    def embed_documents(text_list) -> list[list[float]]:
        OpenAIEmbeddingEngine._init_engine()
        print(f"开始处理embedding，输入大小: {len(text_list)}")
        doc_result = OpenAIEmbeddingEngine.EMBEDDING_ENGINE.embed_documents(text_list)
        print(f"完成处理embedding，输出大小: {len(doc_result)}")
        return doc_result
