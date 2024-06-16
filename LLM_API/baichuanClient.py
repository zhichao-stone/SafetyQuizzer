import requests
import json
import re
#有请求频率限制
# 百川大模型


class BaichuanClient:
    def __init__(self, info):
        self.api_key = info["api_key"]
        self.url = "https://api.baichuan-ai.com/v1/chat/completions"
    
    def call_api(self, question, **input_kwargs):
        json_data = json.dumps({
            "model": "Baichuan2-Turbo",
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ],
            "stream": True
        })
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }
        
        response = requests.post(self.url, data=json_data, headers=headers, timeout=60)
        content_matches = re.findall(r'"content":"(.*?)"', response.text)
        answer = ""
        if content_matches:
            for content_match in content_matches:
                answer += content_match
        else:
            print("未找到匹配的内容")
        return answer






