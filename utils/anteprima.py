import markdown
import json

RESPONSE_FILE = "out/responses.jsonl"
ANTEPRIMA_FILE = "out/anteprima.html"

def risposta_to_html(md: str) -> str:
	return markdown.markdown(md, extensions=['fenced_code', 'tables'])


def load_prompts():
	with open("prompts.json", encoding="utf-8") as f:
		prompt_list = json.load(f)
		return {p["id"]: p for p in prompt_list}

with open('out/responses.jsonl', "r", encoding="utf-8") as f:
	first_line = f.readline()


def convert_all_responses():
	prompt_list = load_prompts()
	css = """
		body, .answer {
			-webkit-print-color-adjust: exact;
			print-color-adjust: exact;
		}
		.answer {
			border: 2px solid #ccc;
			border-radius: 6px;
			padding: 16px 20px;
			margin: 16px 0;
			background-color: #a2e0d6;
			box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
			font-size: 0.9em;
		}
		.answer > :first-child {
			margin-top: 0;
		}
		.answer > :last-child {
			margin-bottom: 0;
		}
	"""
	with open(ANTEPRIMA_FILE, "w", encoding="utf-8") as write:
		html = f"""
			<style>
				{css}
			</style>
		"""
		write.write(html)
		with open(RESPONSE_FILE, "r", encoding="utf-8") as read:
			i = 0
			for line in read:
				response = json.loads(line)
				prompt_id = response["prompt_id"]
				prompt = prompt_list[prompt_id]
				html = f"""
					<h1>Prompt {prompt_id}</h1>
						<h2>Quesito</h2>
						<p>{prompt["prompt"]}</p>
					<h2>Dettagli</h2>
						<ul>
							<li>Categoria: {prompt["category"]}</li>
							<li>GPU utilizzata: {response["gpu"]}</li>
							<li>Tempo di generazione della risposta: {response["generation_time"]}</li>
							<li>Token generati: {response["token_number"]}</li>
						</ul>
					<h2>Risposta</h2>
						<div class="answer">
							{risposta_to_html(response["response"])}
						</div>
				"""
				write.write(html)



convert_all_responses()


print("done.")
