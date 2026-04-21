# Skill: Staging Builder

Purpose: progettare e generare le tabelle staging del datamart come file SQLX
Dataform, a partire dalla mappa unificata prodotta da `input-reader`.

---

## Principi delle tabelle staging

Le tabelle staging:
- **Selezionano e rinominano** campi dalla sorgente (no calcoli aggregati)
- **Filtrano** solo i record necessari per il layer public
- **Non calcolano KPI** — solo preparazione e pulizia dati
- **Referenziano** tabelle sorgente del dataset normalised, staging o raw
- Hanno `type: table` o `type: incremental` in Dataform

---

## Decisioni di design

Per ogni tabella staging da generare, decidi:

### 1. Tipo tabella (`type`)
| Scenario | Tipo consigliato |
|---|---|
| Dati storici completi, replace totale | `table` |
| Dati con partizione data, aggiornamento incrementale | `incremental` |
| Solo join/lookup senza volume elevato | `table` |

### 2. Partitioning
Se la tabella ha un campo data (es. `subscription_date`, `purchase_date`):
```sqlx
partitionBy: "DATE(<campo_data>)"
```

### 3. Clustering
Se la tabella è filtrata frequentemente per brand o customer:
```sqlx
clusterBy: ["brand_code", "customer_code"]
```

### 4. Dipendenze da staging esistente
Se la sorgente è già una tabella staging di produzione, referenziala direttamente:
```sql
FROM ${ref("staging", "<tabella_esistente>")}
```
Non duplicare la logica normalised→staging già implementata in produzione.

---

## Struttura SQLX staging

```sqlx
config {
  type: "table",
  schema: "dm_<nome_datamart>",
  name: "<nome_tabella>",
  description: "<descrizione business>",
  tags: ["dm_<nome_datamart>", "staging"],
  bigquery: {
    partitionBy: "DATE(<campo_data>)",    // solo se applicabile
    clusterBy: ["brand_code", "customer_code"]
  }
}

SELECT
  -- === Identifiers (HK) ===
  S.<campo_sorgente>                      AS <campo_output>,

  -- === Dimensional attributes ===
  S.<campo_sorgente>                      AS <campo_output>,

  -- === Timestamps ===
  DATE(S.<campo_sorgente>)                AS <campo_output>,

  -- === Flag ===
  S.<flag_field>

FROM ${ref("<schema_sorgente>", "<tabella_sorgente>")} AS S

LEFT JOIN ${ref("<schema_2>", "<tabella_2>")} AS T2
  ON S.<chiave> = T2.<chiave>

WHERE
  <filtro_necessario>   -- solo i record utili al datamart
```

---

## Regole di naming

- Schema DM: `dm_<nome_datamart>` in snake_case (es. `dm_customer_fidelity`)
- Nome tabella: stesso nome dell'entità sorgente o `<entità>_<qualificatore>`
- Nomi colonne: `snake_case`, coerenti con il requisito
- Alias espliciti sempre (no `SELECT *`)
- Commenti per ogni blocco logico

---

## Checklist per ogni tabella staging

- [ ] `type` corretto (table/incremental)
- [ ] `schema: "dm_<nome>"` dichiarato
- [ ] `tags` con nome datamart e layer
- [ ] Tutti i campi `defined_by: HK` presenti (sono dalla sorgente)
- [ ] `partitionBy` se c'è un campo data ad alto volume
- [ ] `clusterBy` se filtrata per brand/customer
- [ ] `WHERE` riduce il volume al necessario
- [ ] Nessun KPI calcolato (quelli vanno nel public layer)
- [ ] `${ref()}` usato per tutti i riferimenti a tabelle
