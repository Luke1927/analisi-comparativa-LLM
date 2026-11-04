import json

codes = {
	"writing": 100,
	"roleplay": 200,
	"reasoning": 300,
	"math": 400,
	"coding": 500,
	"extraction": 600,
	"stem": 700,
	"humanities": 800,
}


def generate_new_prompts(filename):
	new_prompt_list = []
	with open(filename, "r", encoding="utf-8") as file:
		for line in file:
			line = line.strip()
			if not line:
				continue
			prompt = json.loads(line)
			category = prompt["category"]

			if not (category in codes):
				raise ValueError(f"Categoria non riconosciuta: {category}")
			index = codes[category]
			codes[category] = index + 1
			new_prompt = {
				"id": index,
				"category": category,
				"language": "en",
				"prompt": prompt["turns"][0]
			}
			new_prompt_list.append(new_prompt)
	return new_prompt_list


def sort(prompt_list):
	sorted_prompt_list = sorted(prompt_list, key=lambda x: x["id"])
	return sorted_prompt_list


# main
prompts = generate_new_prompts("local/MT_bench.jsonl")
prompts = sort(prompts)
data = json.dumps(prompts, ensure_ascii=False, indent="\t")
with open("dataset/prompts-en.json", "w", encoding="utf-8") as file:
	file.write(data)
print("done.")
