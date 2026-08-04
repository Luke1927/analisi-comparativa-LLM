import os

from huggingface_hub import snapshot_download

os.environ["HF_XET_HIGH_PERFORMANCE"] = "1"

host_type = os.getenv("HOST_TYPE", "workstation").lower()

if host_type == "workstation":
	print("Scaricamento modelli dalla workstation...")
	models_to_download = [
		"meta-llama/Llama-3.2-1B-Instruct",
		"Qwen/Qwen2.5-1.5B-Instruct",
		"microsoft/Phi-3-mini-4k-instruct",
		"google/gemma-2-2b-it",
		"meta-llama/Llama-3.2-3B-Instruct"
	]
else:
	print("Scaricamento modelli da casa...")
	models_to_download = [
		"HuggingFaceTB/SmolLM2-135M-Instruct",
		"HuggingFaceTB/SmolLM2-360M-Instruct",
		"Qwen/Qwen2.5-0.5B-Instruct",
	]

for repo_id in models_to_download:
	print(f"\nScaricamento di {repo_id} in corso...")
	try:
		snapshot_download(repo_id=repo_id, max_workers=8)
	except Exception as e:
		print(f"\nErrore durante lo scaricamento di {repo_id}:\n\t{e}")


print(f"\n{"="*29}\n|| Scaricamento completato ||\n{"="*29}")
