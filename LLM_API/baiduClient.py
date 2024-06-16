import os
import qianfan


class BaiduClient:
    def __init__(self, info):
        os.environ["QIANFAN_ACCESS_KEY"] = info["api_key"]
        os.environ["QIANFAN_SECRET_KEY"] = info["secret_key"]
        self.client = qianfan.ChatCompletion(model="ERNIE-Bot")

    def call_api(self, question, **input_kwargs):
        answer = self.client.do(
            messages=[
                {"role": "user", "content": question}
            ],
            **input_kwargs
        )
        return answer["body"]["result"]