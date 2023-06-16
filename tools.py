from langchain.embeddings import OpenAIEmbeddings
import chromadb
import uuid
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from tqdm import tqdm
from langchain.llms import OpenAI
import textwrap

llm = OpenAI(openai_api_key="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",temperature=0,max_tokens=1024)

embeddings = OpenAIEmbeddings(openai_api_key="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")

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=r"C:\Users\sisplayer\Downloads"
))

collection = client.get_or_create_collection (
    name='test1'
)

def get_embeddings_from_openai(text_content,openai_api_key="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"):
    doc_result = embeddings.embed_documents([text_content])
    return doc_result[0]

with open(r"C:\Users\sisplayer\Downloads\data.txt",'r',encoding='utf-8') as f:
    content = f.read()

text_list = [i for i in content.split('\n') if i!='']

def save_text_to_vecstore(data):
    for i in tqdm(data):
        collection.add(
            documents=[i],
            embeddings=[get_embeddings_from_openai(i)],
            ids = [uuid.uuid4().hex]
        )

def ask_question(question,query_keyword=None):
    if not query_keyword:
        query_keyword=question
    results = collection.query(
        query_embeddings = [get_embeddings_from_openai(query_keyword)],
        n_results=50
    )
    results = results['documents'][0]
    
    
    max_results = []
    for result in results:
        if len(''.join(max_results))>1000:
            break
        else:
            max_results.append(result)        
    text_resource = '\n'.join(max_results)

    
    prompt = textwrap.dedent(f"""
    <resource>
    {text_resource}
    </resource>
    -----------------------------------------
    请根据上述<resource>标签内的材料回答以下问题：
    {question}
    """)
    print(prompt)
    print(llm(prompt))

save_text_to_vecstore(text_list)
client.persist()