import tiktoken

from constants.common import CommonConstants


class TokenUtil:
    @staticmethod
    def count_token(
        string: str,
        model_name: str = CommonConstants.openai_llm_model_name
    ) -> int:
        encoding = tiktoken.encoding_for_model(model_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
