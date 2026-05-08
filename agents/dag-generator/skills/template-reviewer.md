# Skill: Template Reviewer

Purpose: identificare il template corretto e derivare l'elenco minimo di
variabili richieste per generare un DAG coerente con il repository corrente.

---

## Obiettivo

Prima di generare codice, devi leggere il repository target e capire quale
pattern locale usare. Non partire mai da supposizioni.

---

## Cosa cercare

### Per DAG `cdf`

Controlla nell'ordine:
- `dags/cdf/template/template_dag.py`
- `dags/cdf/template/dynamic_pipeline_template_dag.py`
- `utils/cdf_utils.py`
- `dags/cdf/**/configs/*_config.yml`

Estrarre almeno:
- costanti obbligatorie (`DATA_SOURCE`, `ASSET_NAME`, `NAMESPACE`, `VERSION`)
- convenzioni `default_args`
- regole per `editable_params`
- naming del file config e posizione cartella `configs/`

### Per DAG `cf`

Controlla nell'ordine:
- `dags/cf/template/template_dag.py`
- `utils/cf_utils.py`
- `dags/cf/**/configs/*_config.yml`

Estrarre almeno:
- parametri HTTP richiesti (`function_url`, `method`, `timeout`, `authenticated`)
- struttura payload/headers
- costanti di audit/logging (`ASSET_NAME`, `PROCESS_NAME`, `PLATFORM_NAME`)

### Per DAG `df`

Se l'utente non ha ancora specificato bronze/semantic, cerca entrambi:
- `dags/df_bronze/template/template_dag.py`
- `dags/df_bronze/template/template_cf_dag.py`
- `dags/df_semantic/template/template_dag.py`
- `utils/df_utils.py`

Estrarre almeno:
- tipo di upstream atteso (`cdf`, `cf`, nessuno)
- parametri Dataform (`REPOSITORY_ID`, `DF_TAGS`, `DF_WORKFLOW_INVO`)
- forma di `SOURCE_TABLE` e `DESTINATION_TABLE`

---

## Output atteso da questa skill

Costruisci una scheda decisionale come questa:

| Campo | Valore |
|---|---|
| `dag_type` | `cdf` / `cf` / `df_bronze` / `df_semantic` |
| `template_path` | path del template scelto |
| `utils_path` | utility primaria da riusare |
| `config_required` | yes/no |
| `config_path_pattern` | cartella e naming atteso |
| `required_questions` | elenco domande minime da fare all'utente |
| `similar_examples` | 1-3 DAG simili letti dal repo |

Questa scheda serve a minimizzare le domande e a evitare generazione fuori
standard.

---

## Regole decisionali

- Se esiste un template dedicato per il caso specifico, usa quello invece di un
  template più generico.
- Se il DAG DF ha upstream Cloud Function, preferisci il template bronze
  specifico per `cf` quando presente.
- Se nel repository trovi già 1-2 esempi concreti più vicini del template,
  usali come riferimento di naming e commenti.
- Se mancano template o utility per il caso richiesto, dichiaralo prima di
  procedere alla generazione.