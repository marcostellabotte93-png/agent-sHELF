# Skill: PowerShell Runner

Purpose: descrive il runner PowerShell che esegue materialmente la documentazione
chiamando le API GCP (BigQuery, Data Lineage, Dataform).

Il runner si trova in `skills/dataset_documenter/generate_doc.ps1` nel workspace
del progetto, **non** in questo repository. Questo file ne documenta interfaccia,
parametri e output atteso.

## Script

```
skills/dataset_documenter/generate_doc.ps1
```

## Parametri

| Parametro | Obbligatorio | Default | Descrizione |
|---|---|---|---|
| `-ProjectId` | ✅ | — | ID progetto GCP |
| `-Dataset` | ✅ | `staging` | Nome dataset BigQuery da documentare |
| `-Location` | ✅ | `EU` | Regione BigQuery (`EU`, `US`, ecc.) |
| `-WorkspacePath` | ✅ | `.` | Root del workspace (cartella corrente) |
| `-RequiredAccount` | ❌ | SA configurato | Service account da usare |
| `-KeyFile` | ❌ | `.\secrets\gcp\...key.json` | Path al file JSON della chiave SA |
| `-OutputDir` | ❌ | `.\projects\dataset_documentation` | Cartella di output |
| `-DataformRepo` | ❌ | — | Nome del repository Dataform |
| `-DataformLocation` | ❌ | — | Regione GCP del repository Dataform |
| `-DataformWorkspace` | ❌ | `enterprise` | Workspace Dataform da leggere |
| `-DataformSqlxPrefix` | ❌ | `definitions/<project>` | Path prefix dei file SQLX |

## Invocazione

```powershell
.\skills\dataset_documenter\generate_doc.ps1 `
  -ProjectId   <project_id> `
  -Dataset     <dataset> `
  -Location    EU `
  -WorkspacePath . `
  -DataformRepo       <repo_name> `
  -DataformLocation   <region> `
  -DataformWorkspace  <workspace> `
  -DataformSqlxPrefix definitions/<project_prefix>
```

## Output atteso su stdout

```
AUTH_OK=true
QUERY_PERMISSION_OK=true
OBJECTS=<n>
COLUMNS=<n>
JOIN_RULES=<n>
FILE_CREATED=.\projects\dataset_documentation\<dataset>_doc.md
SQL_QUERIES_RECOVERED=<n>
DATAFORM_SQLX_LOADED=<n>
CROSS_LAYER_LINKS=<n>
LINEAGE_API=ok
WARNINGS=<lista warning non bloccanti>
RUN_PARAMETERS=...
```

## Indicatori chiave

| Indicatore | Significato |
|---|---|
| `AUTH_OK=true` | Autenticazione service account riuscita |
| `DATAFORM_SQLX_LOADED` | File SQLX letti dal repo Dataform (fonte SQL primaria) |
| `SQL_QUERIES_RECOVERED` | Tabelle con SQL disponibile (SQLX o view definition) |
| `CROSS_LAYER_LINKS` | Dipendenze cross-dataset confermate via Data Lineage API |
| `LINEAGE_API=ok` | Cloud Data Lineage API raggiungibile |

## Fonti dati

| Fonte | API | Dati estratti |
|---|---|---|
| BigQuery INFORMATION_SCHEMA | BigQuery REST API | Tabelle, colonne, view definitions, join rules |
| Cloud Data Lineage API | `datalineage.googleapis.com/v1` | Cross-layer links (staging → public) |
| Dataform API | `dataform.googleapis.com/v1beta1` | File SQLX (testo completo query) |

## Requisiti di sistema

- PowerShell 5.1+
- `gcloud` CLI installato e nel PATH
- Permessi GCP minimi sul service account:
  - `bigquery.tables.get` / `bigquery.tables.list` / `bigquery.datasets.get`
  - `datalineage.processRuns.list`
  - `dataform.repositories.get` / `dataform.workspaces.get`

## Troubleshooting

**`AUTH_OK=false`** — Verificare path e validità del file JSON della chiave SA.

**`DATAFORM_SQLX_LOADED=0`** — Il path `definitions/<prefix>/<dataset>/` non esiste
nel workspace. Verificare `-DataformSqlxPrefix` e `-DataformWorkspace`.

**`CROSS_LAYER_LINKS=0`** — La Data Lineage API potrebbe non avere processato
le esecuzioni Dataform. Verificare che `datalineage.googleapis.com` sia abilitata.

**`SQL_QUERIES_RECOVERED < OBJECTS`** — Alcune tabelle non hanno un file SQLX
con lo stesso nome. Verificare la corrispondenza nome tabella ↔ nome file `.sqlx`.
