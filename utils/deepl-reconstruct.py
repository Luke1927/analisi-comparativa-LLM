import json

PROMPT_EN_FILE = "prompts.json"
PROMPT_IT_FILE = "prompts-it.json"
QUERIES_EN_FILE = "queries-en.txt"
QUERIES_IT_FILE = "queries-it.txt"


def load_en_prompt():
	with open(PROMPT_EN_FILE, "r", encoding="utf-8") as f:
		prompt_list = json.load(f)
		print(f"Loaded a total of {len(prompt_list)} prompts")
		return prompt_list


def load_it_queries():
	query_list = []
	query = ""
	with open(QUERIES_IT_FILE, "r", encoding="utf-8") as f:
		for rawline in f:
			line = rawline.strip()
			if line == "":
				continue
			elif line == "---":
				query_list.append(query)
				query = ""
			else:
				query = query + rawline
		query_list.append(query)

	print(f"Loaded a total of {len(query_list)} queries")
	return query_list


def reconstruct_prompts():
	prompt_list = load_en_prompt() # inizia in inglese, diventa in italiano
	it_query_list = load_it_queries()
	for prompt, it_query in zip(prompt_list, it_query_list, strict=True):
		prompt["language"] = "it"
		prompt["prompt"] = it_query

	with open(PROMPT_IT_FILE, "w", encoding="utf-8") as f:
		json.dump(prompt_list, f, ensure_ascii=False, indent="\t")


reconstruct_prompts()
print("done.")
