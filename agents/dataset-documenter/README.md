# Dataset Documenter

| ID | dataset-documenter |
|---|---|
| Categoria | analytics |
| Versione | 1.0.0 |
| Autore | team-data |
| MCP Server | — |

Agente specializzato nella documentazione read-only di dataset BigQuery.
Estrae schema, join rules, KPI, lineage cross-layer e query SQL sorgente da Dataform.
Produce un documento markdown strutturato pronto per agenti datamart downstream.

---

## Cosa fa

- Documenta tabelle e viste BigQuery (schema completo, tipi, nullable, semantic role)
- Inferisce join rules tra oggetti dello stesso dataset
- Scopre KPI e formula dai metadati e dalle view definition
- Recupera il testo SQL completo leggendo i file SQLX dal repo Dataform
- Mappa le dipendenze cross-layer (es. `staging` → `public`) via Cloud Data Lineage API
- Produce un documento markdown in 12 sezioni usabile da agenti datamart

## Modalità operativa

**Strettamente read-only.** Nessuna scrittura su BigQuery o GCP.
Usa un service account dedicato con soli permessi di lettura.

---

## Skills

### Core (sempre attive)

| File | Contenuto |
|---|---|
| `agent.md` | System prompt, fasi operative, regole |

### Extended (on-demand con `get_skill`)

| ID | Descrizione |
|---|---|
| `analysis-playbook` | Metodologia di analisi, order of operations, quality gates |
| `auth-and-guardrails` | Autenticazione service account, read-only policy, log events |
| `output-template` | Contratto markdown 12 sezioni, naming, quality rules |
| `powershell-runner` | Interfaccia del runner PS1, parametri, output atteso, troubleshooting |

---

## Come attivarlo

```
list_agents → get_agent("dataset-documenter")
```

Durante la sessione, carica le skill specializzate:

```
get_skill("dataset-documenter", "analysis-playbook")
get_skill("dataset-documenter", "powershell-runner")
```

---

## Requisiti

- PowerShell 5.1+ con `gcloud` CLI nel PATH
- Service account GCP con ruoli: `bigquery.metadataViewer`, `datalineage.viewer`, `dataform.viewer`
- Chiave JSON del service account in `secrets/gcp/` (mai committata)
- API GCP abilitate: BigQuery, Cloud Data Lineage, Dataform
