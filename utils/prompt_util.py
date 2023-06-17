import textwrap
from constants.common import CommonConstants

from utils.token_util import TokenUtil


class PromptUtil:
    TEMPLATE = textwrap.dedent("""<resource>
                                            {text_resource}
                                            </resource>
                                            -----------------------------------------
                                            请根据上述<resource>标签内的材料回答以下问题：
                                            {question}""")

    @staticmethod
    def complete_prompt(question, text_resource):
        prompt = PromptUtil.TEMPLATE.format(
            text_resource=text_resource,
            question=question
        )
        return prompt

    @staticmethod
    def construct_max_prompt(question, query_results):
        valid_prompt = ""
        max_token_for_prompt = CommonConstants.max_token_for_model - CommonConstants.max_token_for_completion
        for i in range(len(query_results)):
            prompt = PromptUtil.complete_prompt(
                question,
                '\n'.join(query_results[:i])
            )
            if TokenUtil.count_token(prompt) > max_token_for_prompt:
                print(f"构筑Prompt完成，采用了{i}条查询结果，总token数为{TokenUtil.count_token(valid_prompt)}，(最大token数为{max_token_for_prompt})...")
                break
            else:
                valid_prompt = prompt
        return valid_prompt
