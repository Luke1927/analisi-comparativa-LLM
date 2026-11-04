import json

PROMPT_EN_FILE = "prompts.json"
QUERIES_EN_FILE = "queries-en.txt"


def load_prompt_texts():
	with open(PROMPT_EN_FILE, "r", encoding="utf-8") as f:
		prompt_list = json.load(f)
		return [p["prompt"] for p in prompt_list]


def extract_queries():
	prompt_texts = load_prompt_texts()
	with open(QUERIES_EN_FILE, "w", encoding="utf-8") as write:
		write.write("\n---\n".join(prompt_texts))


extract_queries()


print("done.")
