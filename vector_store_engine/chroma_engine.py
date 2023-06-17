from typing import List, Optional
import chromadb
from chromadb.config import Settings

from constants.common import CommonConstants

import uuid


class ChromaEngine:
    def __init__(self) -> None:
        self.client = chromadb.Client(
            Settings(
                chroma_db_impl=CommonConstants.chroma_db_impl,
                persist_directory=CommonConstants.persistance_location,
            )
        )

    def get_or_create_collection(self, name):
        self.collection = self.client.get_or_create_collection(name=name)

    def add_single(self, document, embedding, id=uuid.uuid4().hex):
        self.collection.add(
            documents=[document],
            embeddings=[embedding],
            ids=[id]
        )

    def add_batch(self, documents, embeddings, ids:Optional[List[str]]=None):
        if not ids:
            ids = [uuid.uuid4().hex for _ in range(len(documents))]
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids
        )

    def query(self, query_embeddings):
        return self.collection.query(
            query_embeddings=query_embeddings,
            n_results=CommonConstants.n_results
        )
    
    def parse_single_query_result(self, result):
        return result['documents'][0]
