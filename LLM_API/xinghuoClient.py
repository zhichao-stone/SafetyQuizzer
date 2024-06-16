from . import SparkApi


class XinghuoClient:
    def __init__(self, info):
        self.appid = info["appid"]
        self.api_key = info["api_key"]
        self.api_secret = info["api_secret"]

        ### v1.5
        self.domain = "general"
        self.spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"
        # ### v2.0
        # self.domain = "generalv2"
        # self.spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"

    def call_api(self, question, **input_kwargs):
        if len(question) > 8000:
            raise Exception("Question is too long (>8000)")
        else:
            question = [{"role": "user", "content": question}]
            SparkApi.answer = ""
            SparkApi.main(self.appid, self.api_key, self.api_secret, self.spark_url, self.domain, question)
            return SparkApi.answer