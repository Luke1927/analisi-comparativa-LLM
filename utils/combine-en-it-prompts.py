import json

PROMPT_EN_FILE = "dataset/prompts-en.json"
PROMPT_IT_FILE = "dataset/prompts-it.json"
PROMPT = "dataset/prompts.json"


def load_prompt_file(filename):
	with open(filename, "r", encoding="utf-8") as f:
		prompt_list = json.load(f)
		return {p["id"]: p for p in prompt_list}


def combine():
	en_prompt_list = load_prompt_file(PROMPT_EN_FILE)
	it_prompt_list = load_prompt_file(PROMPT_IT_FILE)
	combined_prompt_list = []
	for c in range(100, 801, 100):
		# english
		for p in range(0, 10, 1):
			prompt = en_prompt_list[c + p]
			combined_prompt_list.append(prompt)

		# italian
		for p in range(0, 10, 1):
			prompt = it_prompt_list[c + p + 10]
			combined_prompt_list.append(prompt)
	with open(PROMPT, "w", encoding="utf-8") as f:
		json.dump(combined_prompt_list, f, ensure_ascii=False, indent="\t")



combine()
print("done.")
