# Skill: Input Reader

Purpose: leggere e unificare i due input del datamart generator —
documentazione dataset (dataset-documenter output) e requisiti business (requisito/).

---

## Sorgente 1 — Dataset Documenter Output

**Path:** `projects/dataset_documentation/`
**File:** `*_doc.md` (es. `public_doc.md`, `staging_doc.md`)

### Informazioni da estrarre

Da ogni `*_doc.md` estrai:

1. **Schema per tabella** — da sezione `Schema Tables`:
   - `column_name`, `type`, `nullable`, `semantic_role`
   - Annota quale tabella contiene quale colonna

2. **SQL SQLX completo** — da sezione `Table Generation Queries`:
   - `sql_text` (blocco ```sql```) per ogni tabella con `query_type: dataform_sqlx`
   - Usa questo come fonte primaria per capire la logica di calcolo

3. **Cross-layer lineage** — da sezione `Cross-Layer Linkage`:
   - Mappa `staging.<table>` → `public.<table>`
   - Indica quali staging alimentano quali public

4. **Join rules** — da sezione `Join Rules Matrix`:
   - Join condition, chiavi, cardinalità
   - Usa per costruire le JOIN nelle tabelle aggregazione

5. **KPI Catalog** — da sezione `KPI Catalog`:
   - Formule già documentate da usare nelle tabelle public

---

## Sorgente 2 — Requisiti Business

**Path:** `requisito/`
**Formati supportati:** PDF (estrai testo), MD, TXT, CSV

### Informazioni da estrarre

Per ogni campo nel requisito:

| Attributo | Come estrarlo |
|---|---|
| `field_name` | Nome colonna richiesto |
| `description` | Descrizione business del campo |
| `defined_by` | Chi lo produce: `HK` (sistema sorgente) o `BI` (calcolato) |
| `in_current_flow` | `YES`/`NO` — se già presente nel dataset |
| `used_downstream` | `YES`/`NO` — se usato da sistemi downstream (es. Marketing Cloud) |
| `example_value` | Valore di esempio (utile per inferire il tipo) |

---

## Mappa unificata (output di questa skill)

Costruisci una tabella di mapping con questa struttura:

| required_field | description | defined_by | source_dataset | source_table | source_column | mapping_confidence | notes |
|---|---|---|---|---|---|---|---|
| `customer_id` | Heroku ID | HK | staging | privacy_customer | customer_id | high | exact match |
| `cross_purchases_amount` | Importo cross-channel | BI | public | customer_fidelity_kpi | cross_purchases_amount | high | SQLX disponibile |
| `favourite_store_node` | Store preferito | BI | — | — | — | low | logica da inferire |

**mapping_confidence:**
- `high` — campo trovato con nome esatto nel documenter
- `medium` — campo trovato con nome simile o logica deducibile dal SQLX
- `low` — campo non trovato, da inferire o documentare come gap
- `gap` — campo richiesto senza sorgente identificabile

---

## Gap analysis

Dopo aver costruito la mappa, calcola:
- **Copertura totale**: `(high + medium) / total_required * 100`
- **Gap bloccanti**: campi con `defined_by: BI` e `mapping_confidence: gap`
  (non possiamo calcolarli senza logica esplicita)
- **Gap accettabili**: campi `in_current_flow: NO` già documentati come fuori scope

Segnala i gap bloccanti all'utente prima di procedere alla generazione SQL.
