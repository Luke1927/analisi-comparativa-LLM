import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from huggingface_hub import scan_cache_dir
from models import model_list


def get_executable_models():
	cache_info = scan_cache_dir()
	cached = {repo.repo_id for repo in cache_info.repos if repo.repo_type == "model"}

	missing = [m for m in model_list if m not in cached]
	if missing:
		print("ATTENZIONE: questi modelli non risultano scaricati (esegui prima download_models.py):")
		for m in missing:
			print(f"  - {m}")

	models_to_exec = [m for m in model_list if m not in missing]
	return models_to_exec


def load_model(model_name):
	#model_name = "Qwen/Qwen2.5-0.5B-Instruct"
	#model_name = "HuggingFaceTB/SmolLM2-135M-Instruct"
	print(f"Caricamento di {model_name}...")
	quant_config = BitsAndBytesConfig(
		load_in_4bit=True,
		bnb_4bit_compute_dtype=torch.float16,
		bnb_4bit_quant_type="nf4",
	)
	tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
	model = AutoModelForCausalLM.from_pretrained(
		model_name,
		quantization_config=quant_config,
		device_map="auto",
		local_files_only=True
	)

	print("Modello caricato. Device del modello:", model.device)
	device_map = getattr(model, "hf_device_map", None)
	if device_map:
		print("Device map (multi-device):", device_map)
	else:
		print("Modello interamente su un singolo device:", model.device)


	return model, tokenizer



def evaluate_model(model, tokenizer, prompts):
	# INPUT
	messages = [
		#{"role": "user", "content": "Spiegami in due frasi cos'è un large language model."}
		{"role": "user", "content": "What's the Capital of the US?"}
		#{"role": "user", "content": "Explain in two sentences what's a large language model."}
	]
	inputs = tokenizer.apply_chat_template(
		messages,
		add_generation_prompt=True,
		return_tensors="pt",
		return_dict=True,
	).to(model.device)


	# OUTPUT
	output = model.generate(
		**inputs,
		max_new_tokens=200,
		do_sample=False,
		#do_sample=True,
		#temperature=0.7,
		#top_p=0.9,
		pad_token_id=tokenizer.eos_token_id,
	)
	response = tokenizer.decode(
		output[0][inputs["input_ids"].shape[1]:],
		skip_special_tokens=True
	)
	print("\n--- Risposta ---")
	print(response)



def main():
	models_to_exec = get_executable_models()
	for model in models_to_exec:
		print(model)
	print("done.")

main()
