from . import baichuanClient, baiduClient, xinghuoClient, xverseClient, zhipuClient, qwenClient
from .llm_settings import LLM_SETTINGS


ERROR_INFOMATION = "模型API未正常给出回复"
used_models = [info["name"] for info in LLM_SETTINGS.values()]

class LLM_Client:
    def __init__(self, model_info):
        self.client = None
        self.model_name = model_info["name"].lower()
        if self.model_name not in used_models:
            raise Exception(f"Do not support model {self.model_name}, please choose from {used_models}")
        else:
            if self.model_name in ["baichuan"]:
                self.client = baichuanClient.BaichuanClient(model_info)
            elif self.model_name in ["wxyy"]:
                self.client = baiduClient.BaiduClient(model_info)
            elif self.model_name in ["xunfeixh"]:
                self.client = xinghuoClient.XinghuoClient(model_info)
            elif self.model_name in ["xverse"]:
                self.client = xverseClient.XVerseClient(model_info)
            elif self.model_name in ["chatglm"]:
                self.client = zhipuClient.ZhipuClient(model_info)
            elif self.model_name in ["qianwen", "qwen"]:
                self.client = qwenClient.QWenClient(model_info)
    
    def chat(self, question, **input_kwargs):
        if self.client is None:
            raise Exception("Model Error!")
        else:
            answer = ""
            try:
                answer = self.client.call_api(question, **input_kwargs)
            except Exception as e:
                print(e)
                answer = f"{ERROR_INFOMATION}，错误信息: {e}"
            return answer
