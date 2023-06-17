import os
import re
from typing import Optional,List

from constants.common import CommonConstants


class TextLoader:
    def __init__(self, folder_path: Optional[str] = None) -> None:
        self.folder_path = folder_path
        self.content: List[str] = []
        self.load_content()
        self.clean_content()
        self.format_content()

    def load_content(self):
        print(f"开始读取文件...")
        if not self.folder_path:
            self.folder_path = CommonConstants.input_files_location
        for i in os.listdir(self.folder_path):
            if os.path.splitext(i)[-1].lower() == '.txt':
                with open(os.path.join(self.folder_path, i), 'r', encoding='utf-8') as f:
                    self.content.extend(f.read().split('\n'))

    def clean_content(self):
        self.content = [i.strip() for i in self.content]
        self.content = [i for i in self.content if i != '']
        self.content = [i for i in self.content if len(i) >= CommonConstants.content_min_length]
        self.content = [i for i in self.content if not re.match(r"\d+年\d+月\d+日.*", i)]
        self.content = list(set(self.content))

    def format_content(self):
        self.text = '\n'.join(self.content)

    def get_text_load_result(self):
        return self.text
