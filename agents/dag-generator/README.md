# DAG Generator

Agente VS Code per la generazione guidata di DAG Airflow basati sui template già
presenti nel repository target.

---

## Cosa fa

1. Chiede che tipo di DAG bisogna creare: `cdf`, `cf` o `df`
2. Se necessario, chiede il sottotipo corretto (`bronze` o `semantic` per i DAG DF)
3. Legge i template e le `utils` già presenti nel repository corrente
4. Raccoglie le variabili minime necessarie con uno skill dedicato all'intervista utente
5. Genera il DAG e gli eventuali file config multi-environment
6. Esegue una validazione finale su struttura, naming e formattazione

---

## Quando usarlo

- Devi creare un nuovo DAG mantenendo gli stessi pattern del progetto
- Vuoi evitare errori di naming, folder placement o config multi-env
- Vuoi un flusso guidato a domande invece di scrivere il DAG da zero

---

## Flusso di lavoro

### 1. Classificazione

L'agente ti chiede che DAG vuoi creare:
- `cdf`
- `cf`
- `df`

Se scegli `df`, l'agente ti chiede anche se è:
- `bronze`
- `semantic`

### 2. Raccolta variabili

L'agente usa una fase dedicata di raccolta input e fa solo le domande che non
riesce a dedurre dai template o da DAG simili. Esempi:

- `dag_id`
- `asset_name`
- folder di destinazione
- `schedule_interval`
- upstream da triggerare
- URL Cloud Function
- `SOURCE_TABLE` e `DESTINATION_TABLE`
- `REPOSITORY_ID` e `DF_TAGS`

### 3. Generazione

L'agente copia il template corretto, sostituisce i placeholder e crea gli
eventuali file config seguendo i pattern locali.

### 4. Validazione finale

L'agente controlla:
- coerenza file/path
- placeholder residui
- import e variabili obbligatorie
- blank lines e formattazione coerenti col template vicino

---

## Skills

| Skill | Scopo |
|---|---|
| `input-collector` | Guida l'intervista utente e costruisce la scheda input minima |
| `template-reviewer` | Analizza template, utils e DAG simili nel repository target |
| `dag-generator` | Genera DAG e config sostituendo solo le variabili necessarie |
| `final-validator` | Esegue la validazione finale, inclusa formattazione e blank lines |

---

## Utilizzo

```text
@dag-generator
```

Oppure con un contesto iniziale:

```text
@dag-generator devo creare un DAG cf per una Cloud Function HTTP
```

---

## Vincoli

- Parte sempre dai template locali prima di generare codice
- Non inventa nuove strutture se il repository contiene già un pattern valido
- Chiede conferma o informazioni mancanti quando un valore non è deducibile
- Mantiene stile, blank lines e organizzazione coerenti con i file già presenti