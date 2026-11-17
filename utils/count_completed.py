import json

RESPONSE_FILE = "out/responses.jsonl"

def compute_analysis():
	completed = {}
	gpu_inconsistency = False
	exceeding_tokens = False
	with open(RESPONSE_FILE, "r", encoding="utf-8") as file:
		for line in file:
			if line.strip() == "":
				continue

			response = json.loads(line)
			try:
				gpu = response["gpu"]
			except KeyError:
				gpu = "Tesla T4"

			if response["token_number"] > 1024:
				exceeding_tokens = True
			if gpu != "Tesla T4":
				gpu_inconsistency = True
			name = response["model_name"]
			if not name in completed:
				completed[name] = set()
			completed[name].add( response["prompt_id"] )
	return completed, gpu_inconsistency, exceeding_tokens

def print_analysis():
	completed, gpu_inconsistency, exceeding_tokens = compute_analysis()
	if gpu_inconsistency:
		print('Alcune GPU non sono impostate su "Tesla T4"')
	else:
		print('Tutte le GPU sono impostate su "Tesla T4"')

	if exceeding_tokens:
		print("Alcune risposte sono più di 1024 token")
	else:
		print("Tutte le risposte sono al massimo 1024 token")

	for key, value in completed.items():
		print(f"{key} - {len(value)} risposte")


print_analysis()
