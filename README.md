# SafetyQuizzer

### 1. Requirements

##### 1.1 Base Requirements

```
python >= 3.9
torch
transformers
```

##### 1.2 Requirements for LLM API

```
qianfan	 	# ERNIE-3.5
dashscope	# Qwen-turbo
openai		# GPT
zhipuai		# ChatGLM
sseclient	# XVerse
```

 

### 2. Usage

##### 2.1 Retrieve Events

```shell
python main_retrieve_events.py --types [List of Types]
```

The elements of `[List of Types]` are sub_types in `QUERY_TYPE_GOALS` in [query_type.py](query_type.py)

##### 2.2 Generate Questions, Query Target LLMs and Get Responses

```shell
python main_safety_quizzer_query.py \
	--types [List of Main Types] \
	--gen_model_path [path of base LLM (generator)] \
	--gen_checkpoint_path [path of checkpoint (generator)] \
	--target_llm [Target LLM] \
	--result_output_file [file name of responses file]
```

##### 2.3 Evaluate the Responses

```shell
python main_safety_quizzer_evaluate.py \
	--evalutor [LLM as Evaluator] \
	--in_path [file name of responses file]
```

##### 2.4 Calculate Metrics

```shell
python main_calculate_metric.py \
	--target [Target LLM] \
	--evaluators [List of LLMs as Evaluators]
```



