import os
from models import model_list

from huggingface_hub import snapshot_download

os.environ["HF_XET_HIGH_PERFORMANCE"] = "1"

for repo_id in model_list:
	print(f"\nScaricamento di {repo_id} in corso...")
	try:
		snapshot_download(repo_id=repo_id, max_workers=8)
	except Exception as e:
		print(f"\nErrore durante lo scaricamento di {repo_id}:\n\t{e}")


print(f"\n{'='*29}\n|| Scaricamento completato ||\n{'='*29}")
