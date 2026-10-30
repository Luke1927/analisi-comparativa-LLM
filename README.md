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
Eseguire il file `download_models.py`:
```sh
python3 download_models.py
```

Per vedere i modelli scaricati su linux basta eseguire:

```sh
ls -l ~/.cache/huggingface/hub
```

## Login su Hugging-Face
Eseguire questo comando e seguire la procedura richiesta:

```sh
hf auth login
```

# Esecuzione

## Generazione delle risposte
Per eseguire il processo di inferenza dei modelli scaricati, eseguire il file `generate.py`:
```sh
python3 evaluate.py
```

## Valutazione delle AI
> TODO
Per eseguire il processo di valutazione di tutte le risposte generate dalle AI, eseguire il file `evaluate.py`:
```sh
python3 evaluate.py
```

# Anteprima
È stato generato un file di anteprima per visualizzare lo stato di avanzamento del progetto. Fino ad ora si è eseguito su una sessione di Google Colab con gpu Tesla T4 solamente il modello `google/gemma-4-E4B-it`, che si tratta di un modello a 8 miliardi di parametri, ma 4.4 miliardi effettivi, in quanto tale modello fa uso di Per-Layer Embeddings (PLE). Il modello è stato quantizzato a 4 bit (`load_in_4bit=True`), ed è stato fatto girare sui prompt del dataset "MT bench", che è specifico per la valutazione degli LLM, dove ogni prompt è classificato in diverse categorie. Il dataset originale di "MT bench" utilizza una sequenza di prompt, di solito due prompt da eseguire uno dopo l'altro all'interno della stessa "conversazione". Nel nostro progetto abbiamo utilizzato solamente il primo prompt di ogni array `turns`.

In totale sono stati quindi eseguiti 80 prompts, tutti in lingua inglese, e tutti sul modello `google/gemma-4-E4B-it`, attualmente. Il risultato è stato aggregato con un utility script (`preview2.py`) e convertito in un file html (`out/anteprima.html`). Da lì, è bastato aprire il file in browser qualunque e selezionare l'opzione "Stampa su file" per convertirlo in pdf (`out/anteprima.pdf`)
