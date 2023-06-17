import argparse
import os
import re
import sys
from constants.common import CommonConstants
from embeddings.openai_engine import OpenAIEmbeddingEngine
from llms.openai_engine import OpenAILLMEngine
from utils.ichat_util import IchatUtil
from utils.prompt_util import PromptUtil

from utils.text_load_util import TextLoader
from vector_store_engine.chroma_engine import ChromaEngine


class VectorEmbeddingSearch:
    def __init__(self, args):
        if args.proxy:
            self.set_proxy()
        self.set_default_openai_key()
        self.parse_mode(args)

    def set_default_openai_key(self):
        if not os.environ.get(CommonConstants.openai_api_key):
            os.environ[CommonConstants.openai_api_key] = CommonConstants.default_openai_api_key

    def set_proxy(self):
        os.environ['HTTP_PROXY'] = CommonConstants.proxy_address
        os.environ['HTTPS_PROXY'] = CommonConstants.proxy_address

    def parse_mode(self, args):
        if args.add_mode:
            print('进入新增模式...')
            self.add_mode_process()
        elif args.query_mode:
            print('进入查询模式...')
            self.query_mode_process()
        elif args.ichat_mode:
            print('进入ichat查询模式...')
            self.ichat_query_mode_process()
        else:
            print(f'没有输入任何模式,程序退出...')
            sys.exit(-1)

    def ichat_query_mode_process(self):
        db = self._init_db()

        def callback(msg):
            question = msg.text
            question = question.replace('@陈二狗 ', '')
            print(f"收到问题：{question}")
            result = self._query_impl(question, db)
            print(f"处理完毕：{result}")
            msg.user.send(result)
        IchatUtil(callback).start_itchat()

    def _query_impl(self, question, db):
        result = db.query(OpenAIEmbeddingEngine.embed_document(question))
        query_results = db.parse_single_query_result(result)
        valid_prompt = PromptUtil.construct_max_prompt(question, query_results)
        return OpenAILLMEngine.ask(valid_prompt)

    def query_mode_process(self):
        db = self._init_db()
        question = ""
        while True:
            question = input("请输入问题：").strip()
            if question == 'exit':
                break
            print(self._query_impl(question, db), end='\n\n')

    def _init_db(self):
        db = ChromaEngine()
        db.get_or_create_collection(args.collection_name)
        return db

    def get_documents(self):
        self.content = TextLoader(args.input_file_location).content

    def embed_and_save_to_db(self):
        db = self._init_db()
        embeddings = OpenAIEmbeddingEngine.embed_documents(self.content)
        print("开始写入数据库...")
        db.add_batch(
            documents=self.content,
            embeddings=embeddings
        )
        db.client.persist()

    def add_mode_process(self):
        self.get_documents()
        self.embed_and_save_to_db()
        print("处理完成...")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=f"输入文件默认需放在{CommonConstants.input_files_location}目录下，也可自己指定"
    )
    parser.add_argument('-a', '--add_mode', help='进入新增模式', action='store_true')
    parser.add_argument('-q', '--query_mode', help='进入cli查询模式', action='store_true')
    parser.add_argument('-i', '--ichat_mode', help='进入ichat查询模式', action='store_true')
    parser.add_argument('-f', '--input_file_location', help='自行指定输入文件的路径', type=str)
    parser.add_argument('-c', '--collection_name', help='向量数据库的collection名称', default='default', type=str)
    parser.add_argument('-p', '--proxy', help='是否使用代理模式运行脚本', action='store_true')
    args = parser.parse_args()
    VectorEmbeddingSearch(args)
