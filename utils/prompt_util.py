import textwrap
from constants.common import CommonConstants

from utils.token_util import TokenUtil


class PromptUtil:
    TEMPLATE = textwrap.dedent("""<resource>
{text_resource}
</resource>
-----------------------------------------
你回答问题所有可以依据的材料都在上述<resource>标签内
上面的材料不是一篇文章，每一行都是从大数据里面抽取出来的只言片语
你作为一个堪比福尔摩斯的侦探，不会放过每一个细节，你能够尽可能地发现每个独立片段之间的细微关联
并且用你高超的推理能力和想象力产生独到的结论
最重要的是你回答和结论都是源自于材料本身，尽可能不要依赖你本身的知识和经验
而且在回答里面最好告诉我你的回答是由材料哪些部分推理分析产生的
那么问题如下：
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
