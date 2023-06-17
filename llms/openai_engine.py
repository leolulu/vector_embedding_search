from typing import Optional
from langchain import OpenAI

from constants.common import CommonConstants


class OpenAILLMEngine:
    LLM_ENGINE: OpenAI

    @staticmethod
    def _init_engine():
        if 'LLM_ENGINE' not in OpenAILLMEngine.__dict__:
            OpenAILLMEngine.LLM_ENGINE = OpenAI(
                model_name=CommonConstants.openai_llm_model_name,  # type: ignore
                temperature=CommonConstants.temperature,
                max_tokens=CommonConstants.max_token_for_completion
            )

    @staticmethod
    def ask(prompt: str) -> str:
        OpenAILLMEngine._init_engine()
        return OpenAILLMEngine.LLM_ENGINE(prompt)
