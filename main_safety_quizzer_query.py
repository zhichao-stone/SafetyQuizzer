import os
import argparse
from tqdm import tqdm

from query_type import QUERY_TYPE_GOALS
from LLM_API import LLM_Client
from LLM_API.llm_settings import LLM_SETTINGS
from utils import *


def parse_arguments():
    parser = argparse.ArgumentParser(description="main code for SafetyQuizzer")
    ### query generation -- prompts
    parser.add_argument("--types", type=str, nargs="*", default="违法犯罪", choices=[k for k in QUERY_TYPE_GOALS.keys()], help="待检测的安全问题类别")
    parser.add_argument("--max_example_num", type=int, default=3, help="生成评测问题的prompt中，样例问句/事件数量")
    parser.add_argument("--num_each_type", type=int, default=50, help="各类别评测问题生成数量")
    parser.add_argument("--example_data_dir", type=str, default="example_datas")
    ### query existing datas
    parser.add_argument("--use_data", action="store_true", help="use existing datas")
    parser.add_argument("--data_path", type=str, default="[existing datas]")
    ### query generation -- generation model
    parser.add_argument("--gen_model_path", type=str, default="[path of base LLM]", help="the file path of base LLM")
    parser.add_argument("--gen_checkpoint_path", type=str, default="[checkpoint path of fine-tuned LLM]", help="the file path of fine-tuned LLM")
    ### evaluation target
    parser.add_argument("--target_llm", type=str, default="chatglm", choices=LLM_SETTINGS.keys(), help="待检测的目标大模型")
    ### other settings
    parser.add_argument("--result_output_dir", type=str, default="target_llm_responses")
    parser.add_argument("--result_output_file", type=str, default="qa.json")
    parser.add_argument("--tmp_save_step", type=int, default=10)
    
    args = parser.parse_args()
    return args




if __name__ == "__main__":
    ### code arguments
    args = parse_arguments()
    target_llm = args.target_llm
    result_output_path = ""
    if args.result_output_file != "":
        result_output_dir = os.path.join(args.result_output_dir, target_llm)
        if not os.path.exists(result_output_dir):
            os.makedirs(result_output_dir)
        result_output_path = os.path.join(result_output_dir, args.result_output_file)
    tmp_dir = "tmp_data"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    all_queries = []
    if not args.use_data:
        ### use generated questions to evaluate target LLM
        tmp_query_path = os.path.join(tmp_dir, "tmp_queries.json")
        if os.path.exists(tmp_query_path):
            all_queries = load_json(tmp_query_path)
        else:
            from llmtuner.chat import ChatModel
            from prompts_generation import generate_prompts_for_single_type
            ##### read templates, example events and example queries
            example_data_dir = args.example_data_dir
            types = args.types
            templates = load_json(os.path.join(example_data_dir, "query_templates.json"))
            example_events = load_json(os.path.join(example_data_dir, "example_events.json"))
            example_queries = load_json(os.path.join(example_data_dir, "example_queries.json"))

            ##### prompts generation
            all_prompts = []
            for main_type in types:
                nums = split_type_num(args.num_each_type, len(QUERY_TYPE_GOALS[main_type]))
                for i, (sub_type, type_desc) in enumerate(QUERY_TYPE_GOALS[main_type].items()):
                    type_example_events = example_events[sub_type] if sub_type in example_events else []
                    type_example_queries = example_queries[sub_type] if sub_type in example_queries else []
                    prompts = generate_prompts_for_single_type(sub_type, type_desc, templates, type_example_events, type_example_queries, single_style=True, max_example_num=args.max_example_num, num_each_type=nums[i])
                    for p in prompts:
                        all_prompts.append((main_type, sub_type, p))

            ##### query generation
            print("\n############################## 生成评测问题中...... ##############################")
            gen_model_args = {
                "model_name_or_path": args.gen_model_path,
                "checkpoint_dir": args.gen_checkpoint_path,
                "template": "baichuan2"
            }
            gen_model = ChatModel(gen_model_args)
            
            for main_type, sub_type, prompt in tqdm(all_prompts, desc="问题生成中"):
                raw_query_text, _ = gen_model.chat(prompt["prompt"])
                queries = process_gen_query(raw_query_text[0])
                for q in queries:
                    all_queries.append((main_type, sub_type, q))
            dump_json(tmp_query_path, all_queries)

    else:
        ### use existing datas to evaluate target LLM
        data = load_json(args.data_path)
        all_queries = [(q["main_type"], q["sub_type"], q["prompt"]) for q in data]

    ### test target LLM
    print(f"\n############################## 评测目标模型: {target_llm} ...... ##############################")
    llm_info = LLM_SETTINGS[target_llm]
    client = LLM_Client(llm_info)

    all_responses = [] if not os.path.exists(result_output_path) else load_json(result_output_path)
    index = len(all_responses)

    print(f"Start from: {index} / {len(all_queries)}")
    for main_type, sub_type, q in tqdm(all_queries[index:], desc=f"Evaluating {target_llm}"):
        index += 1
        response = client.chat(q)
        all_responses.append({
            "id": index - 1, 
            "main_type": main_type, 
            "sub_type": sub_type, 
            "question": q, 
            "response": response
        })
        if index % args.tmp_save_step == 0:
            dump_json(result_output_path, all_responses)
    
    dump_json(result_output_path, all_responses)