import os

os.environ["HF_XET_HIGH_PERFORMANCE"] = "1"

host_type = os.getenv("HOST_TYPE", "workstation").lower()

if host_type == "workstation" or host_type == "colab":
	model_list = [
		"meta-llama/Llama-3.2-1B-Instruct",
		"meta-llama/Llama-3.2-3B-Instruct",
		"Qwen/Qwen3-1.7B",
		"Qwen/Qwen3-4B",
		"microsoft/Phi-4-mini-instruct",
		"google/gemma-4-E2B-it",
		"google/gemma-4-E4B-it",
	]
else:
	# Modelli di propotipazione per il computer di casa.
	# Non rientreranno nel report finale
	model_list = [
		"HuggingFaceTB/SmolLM2-135M-Instruct",
		"HuggingFaceTB/SmolLM2-360M-Instruct",
		"Qwen/Qwen2.5-0.5B-Instruct",
	]


# Google Colab funziona in sessioni da 12 ore massime,
# e dopo ogni sessione si resetta l'ambiente di sviluppo, cancellando
# tutti gli eventuali modelli scaricati con il nostro `download_models.py`.
# Quindi è inutile scaricare tutti i modelli in anticipo e eseguirli
# tutti insieme dopo. Conviene lavorare con un modello per volta
if host_type == "colab":
	colab_index = int(os.getenv("COLAB_INDEX", "0"))
	model_list = [ model_list[colab_index] ]
