import json
import requests
from sseclient import SSEClient
# 元象XVerse


def process_sse(response):
    # 使用SSEClient处理流式数据
    client = SSEClient(response)

    # 初始化一个空字符串用于拼接内容
    concatenated_data = ""

    # 遍历SSE事件
    for event in client.events():
            data_json = event.data
            # 解析SSE事件的data字段，这里data是一个JSON字符串
            data_dict = json.loads(data_json)

            choices = data_dict.get('choices', [])

            for ch in choices:
                content_data = ch.get('delta', {})
                finish_reason = ch.get('finish_reason', '')
                content = content_data.get('content', '')

                # 还在进行中
                if finish_reason == '':
                    # 拼接内容
                    print(content, end='')
                    concatenated_data += content

                # 结束循环，因为数据流结束了
                elif finish_reason == 'stop':
                    break

                # 被过滤的数据进行处理
                elif finish_reason == 'content_filter':
                    print(content, end='')
                    concatenated_data += "「trigger sensitive」"
                    break

def process_non_sse(response):
    response_content = json.loads(response.content.decode('utf-8'))
    choices = response_content.get('choices', [])
    if len(choices) > 0:
        ch = choices[0]
        print(ch.get("message", {}).get("content", {}))
    return ch.get("message", {}).get("content", {})

def fetch_chat_data(url, api_key, body_data):
    # 构建请求头信息
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',  # 设置请求体类型为 JSON
    }
    try:
        # 发送带有头信息和请求体的 POST 请求
        response = requests.post(url, stream=True, headers=headers, data=json.dumps(body_data))

        # 检查响应状态码
        response.raise_for_status()

        if body_data.get('stream'):
            process_sse(response)
        else:
            return process_non_sse(response)


    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        raise e

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


class XVerseClient:
    def __init__(self, info):
        self.api_key = info["api_key"]
        self.url = "https://api.xverse.cn/v1/chat/completions"

    def call_api(self, question, **input_kwargs):
        body_data = {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ],
            "stream": True
        }
        body_data["stream"] = False
        answer = fetch_chat_data(self.url, self.api_key, body_data)
        return answer