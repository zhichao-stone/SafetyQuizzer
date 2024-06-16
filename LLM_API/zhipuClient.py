from zhipuai import ZhipuAI
# 智谱


class ZhipuClient:
    def __init__(self, info):
        self.client = ZhipuAI(api_key=info["api_key"])
    
    def call_api(self, question, **input_kwargs):
        response = self.client.chat.completions.create(
            # model="glm-4",
            model="glm-3-turbo",
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ],
            # top_p=0.7,
            # temperature=0.95,
            # max_tokens=1024,
            stream=True,
            **input_kwargs
        )

        answer = ""
        for trunk in response:
            for i in trunk.choices[0].delta.content:
                answer = answer + i

        return answer

