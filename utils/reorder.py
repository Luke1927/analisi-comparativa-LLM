import sys
from pathlib import Path

# Adds the parent directory (one level up) to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from models import model_list
import json


RESPONSE_FILE = "out/responses.jsonl"
NEW_RESPONSE_FILE = "out/fixed_responses.jsonl"

def load_responses():
	dic_of_responses = {}
	with open(RESPONSE_FILE, "r", encoding="utf-8") as file:
		for line in file:
			if line.strip() == "":
				continue

			response = json.loads(line)
			if not "gpu" in response:
				response["gpu"] = "Tesla T4"

			name = response["model_name"]
			id = response["prompt_id"]
			new_key = name + str(id)
			dic_of_responses[new_key] = response

	return dic_of_responses

def write_responses():
	response_list = load_responses()
	with open(NEW_RESPONSE_FILE, "a", encoding="utf-8") as file:
		for model_name in model_list:
			for category in range(100, 801, 100):
				for language in range(0, 11, 10):
					for query_number in range(0, 10, 1):
						id = category + language + query_number
						new_key = model_name + str(id)
						response = response_list[new_key]
						line = json.dumps(response, ensure_ascii=False)
						line += "\n"
						file.write(line)

write_responses()
print("done.")
