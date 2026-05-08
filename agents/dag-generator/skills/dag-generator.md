# Skill: DAG Generator

Purpose: generare file DAG e config a partire dal template corretto, sostituendo
solo le variabili necessarie e preservando stile, naming e struttura del repo.

---

## Principi di generazione

1. Copia il template più vicino al caso richiesto.
2. Sostituisci i placeholder mantenendo l'ordine delle costanti.
3. Mantieni commenti, blank lines e struttura `with DAG(...) as dag:` come nel
   template locale.
4. Non reimpaginare blocchi non necessari.
5. Se servono file config, creali nello stesso folder pattern usato dagli altri
   DAG della stessa famiglia.

---

## Checklist per `cdf`

- Crea il file DAG nel dominio corretto sotto `dags/cdf/<dominio>/`
- Crea il file YAML in `configs/<data_source>_config.yml` oppure nel naming già
  usato dal template concreto
- Valorizza:
  - `DATA_SOURCE`
  - `ASSET_NAME`
  - `NAMESPACE`
  - `VERSION`
  - `tags`
  - `schedule_interval`
- Se il template usa config multi-documento YAML, mantieni `version`,
  `start_date`, `end_date`

## Checklist per `cf`

- Crea il file DAG nel dominio corretto sotto `dags/cf/<dominio>/`
- Crea il file YAML config sotto `configs/`
- Valorizza:
  - `DATA_SOURCE`
  - `ASSET_NAME`
  - `PROCESS_NAME`
  - `PLATFORM_NAME`
  - `function_url`
  - `method`
  - `timeout`
  - `authenticated`
  - `payload` o parametri runtime equivalenti
- Se il payload è strutturato, usa il suffisso `_json_decode` quando il
  template locale lo supporta

## Checklist per `df`

- Crea il file DAG sotto `dags/df_bronze/...` o `dags/df_semantic/...`
- Se c'è upstream, configura correttamente `create_trigger_operator(...)`
- Valorizza:
  - `DAG_ID`
  - `ASSET_NAME`
  - `SOURCE_TABLE`
  - `DESTINATION_TABLE`
  - `REPOSITORY_ID`
  - `DF_TAGS` o target equivalenti
  - `DF_WORKFLOW_INVO`
  - `RELEASE_NAME` quando richiesto

---

## Domande da trasformare in valori

Quando l'utente risponde alle domande, trasformale in un dizionario di lavoro:

```text
dag_type:
subtype:
domain:
dag_id:
asset_name:
schedule_interval:
config_name:
function_url_by_env:
payload:
upstream_dag_ids:
source_tables:
destination_tables:
dataform_repository:
tags:
```

Usa questo dizionario come unica fonte prima di scrivere i file.

---

## Regole di scrittura

- Nessun placeholder tipo `your_*` deve rimanere nei file finali.
- Se un valore non è noto, fermati e chiedilo all'utente invece di inventarlo.
- Se trovi una utility locale già pronta, non duplicarla.
- Se devi creare una nuova utility, falla aderire alla stessa struttura delle
  altre `utils/*.py` del repository.