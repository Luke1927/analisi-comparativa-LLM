import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from huggingface_hub import scan_cache_dir
from models import model_list
import json
import os
import time

RESPONSE_FILE = "out/responses.jsonl"

def load_prompts():
	with open("prompts.json", "r", encoding="utf-8") as file:
		data = json.load(file)
	return data


def load_completed_prompts():
	completed = {}
	if not os.path.exists(RESPONSE_FILE):
		return completed
	with open(RESPONSE_FILE, "r", encoding="utf-8") as file:
		for line in file:
			line = line.strip()
			if not line:
				continue
			record = json.loads(line)
			model_name = record["model_name"]
			prompt_id = record["prompt_id"]
			if not (model_name in completed):
				completed[model_name] = []
			if not (prompt_id in completed[model_name]):
				completed[model_name].append(prompt_id)
	return completed


def load_executable_models():
	cache_info = scan_cache_dir()
	cached = {repo.repo_id for repo in cache_info.repos if repo.repo_type == "model"}

	missing = [m for m in model_list if m not in cached]
	if missing:
		print("ATTENZIONE: questi modelli non risultano scaricati (eseguire download_models.py):")
		for m in missing:
			print(f"  - {m}")

	models_to_exec = [m for m in model_list if m not in missing]
	return models_to_exec


def load_model(model_name):
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


def unload_model(model):
	del model
	torch.cuda.empty_cache()


def generate_response(model, tokenizer, prompt_text):
	# INPUT
	message = [
		{"role": "user", "content": prompt_text}
	]
	inputs = tokenizer.apply_chat_template(
		message,
		add_generation_prompt=True,
		return_tensors="pt",
		return_dict=True,
	).to(model.device)


	# OUTPUT
	start = time.time()
	output = model.generate(
		**inputs,
		max_new_tokens=200,
		do_sample=False,
		#do_sample=True,
		#temperature=0.7,
		#top_p=0.9,
		pad_token_id=tokenizer.eos_token_id,
	)
	torch.cuda.synchronize()
	end = time.time()
	generation_time = round(end - start, 2)

	new_tokens = output[0][inputs["input_ids"].shape[1]:]
	token_number = new_tokens.shape[0]

	response = tokenizer.decode(
		output[0][inputs["input_ids"].shape[1]:],
		skip_special_tokens=True
	)

	return response, generation_time, token_number


def main():
	executable_models = load_executable_models()
	prompt_list = load_prompts()

	for model_name in executable_models:
		completed = load_completed_prompts()
		completed_prompts = []
		if model_name in completed:
			completed_prompts = completed[model_name]
		prompts_to_exec = []
		for prompt in prompt_list:
			prompt_id = prompt["id"]
			if not (prompt_id in completed_prompts):
				prompts_to_exec.append(prompt)
		if len(prompts_to_exec) == 0:
			print(f"Modello {model_name} già completato. Avanzamento al prossimo modello\n")
			continue

		try:
			model, tokenizer = load_model(model_name)
		except Exception as e:
			print(f"Errore nel caricamento del modello {model_name}:\n\t{e}\n")
			continue

		print(f"Valutazione del modello {model_name} in corso...")
		prompt_size = len(prompts_to_exec)

		for i in range(prompt_size):
			prompt = prompts_to_exec[i]
			print(f"Calcolo inferenza del prompt {i+1} di {prompt_size}...")
			try:
				response, generation_time, token_number = generate_response(model, tokenizer, prompt["prompt"])
				record = {
					"model_name": model_name,
					"prompt_id": prompt["id"],
					"response": response,
					"generation_time": generation_time,
					"token_number": token_number,
				}
				line = json.dumps(record, ensure_ascii=False)
				line += "\n"
				with open(RESPONSE_FILE, "a", encoding="utf-8") as file:
					file.write(line)
			except OSError as e:
				print(f"Errore di I/O. Esiste la cartella ./out/ ?:\n\t{e}")
			except Exception as e:
				print(f"Errore nella valutazione del modello {model_name} con il prompt #{prompt['id']}:\n\t{e}")

		print()
		unload_model(model)

	print("done.")


# Non penso importeremo mai questo file in altri script,
# ma giusto per essere sicuri seguiamo la prassi standard:
if __name__ == "__main__":
	main()
