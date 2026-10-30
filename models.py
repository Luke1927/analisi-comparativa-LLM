import os

os.environ["HF_XET_HIGH_PERFORMANCE"] = "1"

host_type = os.getenv("HOST_TYPE", "workstation").lower()

if host_type == "workstation" or host_type == "colab":
	model_list = [
		"meta-llama/Llama-3.2-1B-Instruct",
		"meta-llama/Llama-3.2-3B-Instruct",
		"Qwen/Qwen3-1.7B",
		"Qwen/Qwen3-4B",
		"microsoft/Phi-4-mini-instruct",
		"google/gemma-4-E2B-it",
		"google/gemma-4-E4B-it",
	]
else:
	model_list = [
		"HuggingFaceTB/SmolLM2-135M-Instruct",
		"HuggingFaceTB/SmolLM2-360M-Instruct",
		"Qwen/Qwen2.5-0.5B-Instruct",
	]
