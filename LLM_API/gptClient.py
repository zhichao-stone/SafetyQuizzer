import openai
# ChatGPT


class ZhipuClient:
    def __init__(self, info):
        if info["base_url"] != "":
            self.client = openai.OpenAI(api_key=info["api_key"], base_url=info["base_url"])
        else:
            self.client = openai.OpenAI(api_key=info["api_key"])
        self.model = info["model"]
    
    def call_api(self, question, **input_kwargs):
        response = ""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": question}],
                **input_kwargs
            )
        except openai.OpenAIError as e:
            print(e)
        return response

