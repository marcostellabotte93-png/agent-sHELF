# Datamart Generator

Agente VS Code per la generazione di datamart BigQuery pronti per Dataform,
a partire dalla documentazione di dataset (output di `dataset-documenter`) e
dai requisiti business.

---

## Cosa fa

1. Legge i file `*_doc.md` prodotti da `dataset-documenter` in `projects/dataset_documentation/`
2. Legge i requisiti business in `requisito/` (PDF, MD, TXT, CSV)
3. Costruisce una mappa campo-richiesto → campo-disponibile con livello di confidenza
4. Segnala i gap prima di generare
5. Produce file SQLX Dataform organizzati in `staging/` e `public/`
6. Genera un `README.md` con la copertura dei requisiti

---

## Output generato

```
projects/<DM_NAME>/
├── staging/
│   ├── <entità_1>.sqlx        ← selezione/rinomina campi dalla sorgente
│   ├── <entità_2>.sqlx
│   └── ...
├── public/
│   ├── <kpi_table>.sqlx       ← aggregazioni KPI
│   ├── <final_table>.sqlx     ← tabella finale consolidata
│   └── ...
└── README.md
```

---

## Prerequisiti

- Output di `dataset-documenter` disponibile in `projects/dataset_documentation/`
- File di requisiti in `requisito/` (almeno uno)
- Conoscenza del nome del datamart da generare (es. `DM_CustomerFidelity`)

---

## Utilizzo

```
@datamart-generator DM_CustomerFidelity
```

L'agente chiederà conferma prima di procedere se i gap sono > 30% dei campi KPI.

---

## Skills

| Skill | Scopo |
|---|---|
| `input-reader` | Legge e unifica doc + requisiti, costruisce mappa di mapping |
| `staging-builder` | Regole di design per le tabelle staging (tipo, partitioning, clustering) |
| `public-builder` | Logica KPI, pattern aggregazione, checklist tabella finale |
| `dataform-output` | Formato esatto SQLX, struttura cartelle, istruzioni deployment |

---

## Vincoli

- Genera **solo file locali** (.sqlx, .md) — nessun accesso a BigQuery o Dataform
- Non esegue query SQL — usa solo le informazioni dai doc file
- I campi `defined_by: HK` sono copiati direttamente dalla sorgente
- I campi `defined_by: BI` sono calcolati con formule da SQLX o inferite
- I gap non bloccanti sono documentati nel README con motivazione

---

## Compatibilità

Progettato per lavorare in coppia con `dataset-documenter`.
L'output di uno è l'input dell'altro.

```
dataset-documenter → *_doc.md → datamart-generator → *.sqlx
```
