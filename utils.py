import os
import re
import json
import random
import openai


### function for load/save json file
def load_json(path):
    with open(path, "r", encoding="utf-8") as fr:
        datas = json.load(fr)
    return datas

def dump_json(path, obj):
    file_dir = os.path.split(path)[0]
    if file_dir != "":
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
    with open(path, "w", encoding="utf-8") as fw:
        json.dump(obj, fw, ensure_ascii=False, indent=4)


### function for query generation
def split_type_num(num_each_type, sub_type_num):
    ### num_each_type: 每个类别需要生成的评测问题数量
    ### sub_type_num: 每个类别的子类数量
    nums = [num_each_type//sub_type_num for _ in range(sub_type_num)]
    for i in range(num_each_type - sub_type_num*nums[0]):
        nums[i] += 1
    random.shuffle(nums)
    return nums

def process_gen_query(raw_query_text:str):
    queries = []
    raw_queries = raw_query_text.strip().split("\n")
    for raw_query in raw_queries:
        query = re.sub("\d+\.[ ]*", "", raw_query)
        query = re.sub("\[*输出\]*[:|：][ ]*", "", query)
        queries.append(query)
    return queries


### query LLM
def get_response_llm(client:openai.OpenAI, query:str, model:str="gpt-3.5-turbo", messages:list=[], temperature:float=1.0, **kwargs):
    response = ""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages + [{
                "role": "user",
                "content": query
            }],
            temperature=temperature,
            **kwargs
        )
        response = response.choices[0].message.content
    except openai.OpenAIError as e:
        print(f"### ERROR : {e}")
        response = str(e)
    
    return response