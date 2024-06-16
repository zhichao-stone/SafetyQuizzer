import dashscope


class QWenClient:
    def __init__(self, info):
        self.api_key = info["api_key"]
    
    def call_api(self, question, **input_kwargs):
        response = dashscope.Generation.call(
            model="qwen-turbo",
            messages=[{"role": "user", "content": question}],
            api_key=self.api_key,
            result_format = "message"
        )
        if response.status_code == 200:
            answer = response.output.choices[0]["message"]["content"]
            return answer
        else:
            error_message = f"Request ID: {response.request_id} , Status Code : {response.status_code} , Error Code : {response.code} , Error Message : {response.message}"
            raise Exception(error_message)

