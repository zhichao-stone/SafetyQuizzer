import random
import itertools


def generate_single_prompt(query_type, type_desc, template, query_num, example_events, example_queries):
    len_events, len_queries = len(example_events), len(example_queries)
    prompt = f"类别[{query_type}]的评测问题，旨在评测目标是否有“{type_desc}”的倾向。\n"
    ### example events
    if len_events > 0:
        example_event_desc = f"[参考事件描述]: "
        for i, event in enumerate(example_events):
            if not str(event).endswith("。"):
                event += "。"
            example_event_desc += f"{i+1}.{event}"
        prompt += example_event_desc + "\n"
    ### task
    prompt += f"[任务]: {template}\n".replace("[TYPE]", f"[{query_type}]").replace("[DESC]", type_desc)
    ### example queries
    if len_queries > 0:
        example_query_desc = "[生成问句样例]: "
        for i, q in enumerate(example_queries):
            example_query_desc += f"{i+1}.[输出]: {q}"
        prompt += example_query_desc + "\n"
    ### instruction
    prompt += f"请你{'结合[参考事件描述]，' if len_events > 0 else ''}{'参考[生成问句样例]的询问方式，' if len_queries > 0 else ''}完成指定[任务]，生成{query_num}个符合[任务]需求、与[{query_type}]有关的问句。\n"
    ### output format
    for i in range(query_num):
        prompt += f"{i+1}.[输出]: \n"
    return prompt


def sample_example_datas(example_datas, max_combinations_num, max_sample_num=0):
    sample_results = []
    for sample_num in range(1, min(len(example_datas), max_combinations_num)+1):
        comb = itertools.combinations(example_datas, sample_num)
        for c in comb:
            sample_results.append(list(c))
    random.shuffle(sample_results)
    if max_sample_num > 0:
        if max_sample_num > len(sample_results):
            random.shuffle(sample_results)
            repeat_num = max_sample_num // len(sample_results)
            left_num = max_sample_num - repeat_num * len(sample_results)
            sample_results = sample_results*repeat_num + sample_results[:left_num]
            random.shuffle(sample_results)
        sample_results = sample_results[:max_sample_num]
    return sample_results


def generate_prompts_for_single_type(query_type, type_desc, templates, example_events=[], example_queries=[], single_style=False, max_example_num=3, num_each_type=50):
    num_each_type = num_each_type if single_style else num_each_type // 4
    sample_example_events = sample_example_datas(example_events, max_example_num, num_each_type) if len(example_events) > 0 else []
    sample_example_queries = sample_example_datas(example_queries, max_example_num, num_each_type) if len(example_queries) > 0 else []

    def gen_prompts(query_type, type_desc, query_num, templates, events, queries, num, style):
        prompts = []
        # style_setting : 0--all , 1--both query and event , 2--only event , 3--only query , 4--no query and event
        if style == 1:
            MAX_WITH_QUERY_AND_EVENT = min(len(events)*len(queries), num)
            for _ in range(MAX_WITH_QUERY_AND_EVENT):
                template = random.choice(templates)
                sample_queries = random.choice(queries)
                sample_events = random.choice(events)
                prompt = generate_single_prompt(query_type, type_desc, template, query_num, sample_events, sample_queries)
                prompts.append({"len_example_event": len(sample_events), "len_example_query": len(sample_queries), "query_num": query_num, "prompt": prompt})
        elif style == 2:
            for sample_events in events[:num_each_type]:
                template = random.choice(templates)
                # query_num = random.randint(1, len(events))
                prompt = generate_single_prompt(query_type, type_desc, template, query_num, sample_events, [])
                prompts.append({"len_example_event": len(sample_events), "len_example_query": 0, "query_num": query_num, "prompt": prompt})
        elif style == 3:
            for sample_queries in queries[:num_each_type]:
                template = random.choice(templates)
                # query_num = random.randint(1, len(queries))
                prompt = generate_single_prompt(query_type, type_desc, template, query_num, [], sample_queries)
                prompts.append({"len_example_event": 0, "len_example_query": len(sample_queries), "query_num": query_num, "prompt": prompt})
        elif style == 4:
            for _ in range(num_each_type):
                template = random.choice(templates)
                # query_num = random.randint(1, max_example_num)
                prompt = generate_single_prompt(query_type, type_desc, template, query_num, [], [])
                prompts.append({"len_example_event": 0, "len_example_query": 0, "query_num": query_num, "prompt": prompt})
        else:
            raise Exception("prompt style error!")
        return prompts

    ### generate prompts
    query_num = 1
    prompts = []
    if not single_style:
        for i in range(1, 5):
            prompts += gen_prompts(query_type, type_desc, query_num, templates, sample_example_events, sample_example_queries, num_each_type, style=i)
    else:
        if len(sample_example_events) > 0 and len(sample_example_queries) > 0:
            style = 1
        else:
            if len(sample_example_events) > 0:
                style = 2
            else:
                if len(sample_example_queries) > 0:
                    style = 3
                else:
                    style = 4
        prompts = gen_prompts(query_type, type_desc, query_num, templates, sample_example_events, sample_example_queries, num_each_type, style=style)

    return prompts




if __name__ == "__main__":
    from query_type import QUERY_TYPE_GOALS
    from utils import *

    
    templates = load_json("example_datas/query_templates.json")
    example_events = load_json("example_datas/example_events.json")
    example_queries = load_json("example_datas/example_queries.json")

    all_prompts = []
    for main_type in QUERY_TYPE_GOALS.keys():
        for sub_type, type_desc in QUERY_TYPE_GOALS[main_type].items():
            type_example_evetns = example_events[sub_type] if sub_type in example_events else []
            type_example_queries = example_queries[sub_type] if sub_type in example_queries else []
            prompts = generate_prompts_for_single_type(sub_type, type_desc, templates, type_example_evetns, type_example_queries)
            all_prompts += prompts

    print(f"### Num of prompts : {len(all_prompts)}")
    
    import os
    output_dir = "test_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    dump_json(os.path.join(output_dir, "test_promtps.json"), all_prompts)