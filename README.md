# Analisi comparativa degli LLM
In questo progetto andrò a formulare un'analisi tramite una comparazione di diversi modelli linguistici open-weight per confrontarli e proporre il migliore

# Installazione
> Questo progetto usa PyTorch con accelerazione GPU. È necessario installare i driver della scheda video prima di eseguire l'installazione dei pacchetti.

## Installazione pacchetti
Creare e attivare un ambiente virtuale Python:
```sh
python3 -m venv .venv
source .venv/bin/activate
```
Se invece si preferisce utilizzare un ambiente virtuale pre-esistente, è possibile lavorare con quello.

Dopodiché, installare PyTorch per NVIDIA:
```sh
pip install torch --index-url https://download.pytorch.org/whl/cu128
```
o per AMD:
```sh
pip install torch --index-url https://download.pytorch.org/whl/rocm6.3
```

e infine installare il resto dei pacchetti:
```sh
pip install -r requirements.txt
```

## Scaricamento modelli
Eseguire il file `models.py`. Per vedere i modelli scaricati su linux basta eseguire:

```sh
ls -l ~/.cache/huggingface/hub
```
