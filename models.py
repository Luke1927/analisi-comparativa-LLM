import os

os.environ["HF_XET_HIGH_PERFORMANCE"] = "1"

host_type = os.getenv("HOST_TYPE", "workstation").lower()

if host_type == "workstation":
	model_list = [
		"meta-llama/Llama-3.2-1B-Instruct",
		"Qwen/Qwen2.5-1.5B-Instruct",
		"microsoft/Phi-3-mini-4k-instruct",
		"google/gemma-2-2b-it",
		"meta-llama/Llama-3.2-3B-Instruct"
	]
else:
	model_list = [
		"HuggingFaceTB/SmolLM2-135M-Instruct",
		"HuggingFaceTB/SmolLM2-360M-Instruct",
		"Qwen/Qwen2.5-0.5B-Instruct",
	]
