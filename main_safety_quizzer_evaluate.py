import os
import argparse
from tqdm import tqdm
from utils import *
from evaluation import Evaluator
from LLM_API.llm_settings import LLM_SETTINGS


def parse_arguments():
    parser = argparse.ArgumentParser(description="evaluation module for SafetyQuizzer")
    ### model setting for evaluator
    parser.add_argument("--evaluator", type=str, default="chatglm", choices=LLM_SETTINGS.keys())
    ### data path
    parser.add_argument("--in_path", type=str)
    
    args = parser.parse_args()
    return args



if __name__ == "__main__":
    ### code arguments
    args = parse_arguments()
    eval_args = {
        "loading_type": "api",
        "model_args": LLM_SETTINGS[args.evaluator]
    }
    eval = Evaluator(eval_args)

    ### loading qa datas
    question_responses = load_json(args.in_path)

    out_dir = "eval_results"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    file_name = os.path.split(args.in_path)[-1].split(".")[0]
    out_path = os.path.join(out_dir, f"{file_name}_{args.evaluator}.json")
    eval_results = [] if not os.path.exists(out_path) else load_json(out_path)
    index = len(eval_results)

    ### evaluate
    print("\n########################################### 开始评测...... ###########################################")
    print(f"Path of question-response: {args.in_path}")
    print(f"Evaluated: {index} / {len(question_responses)}")

    for qa in tqdm(question_responses[index:]):
        index += 1
        _, res, judgement = eval.evaluate(qa["main_type"], qa["sub_type"], qa["question"], qa["response"])
        eval_results.append({
            **qa,
            **{"eval_judge": judgement}
        })
        if index % 10 == 0:
            dump_json(out_path, eval_results)

    dump_json(out_path, eval_results)