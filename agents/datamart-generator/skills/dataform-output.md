# Skill: Dataform Output

Purpose: definisce il formato esatto dei file SQLX Dataform, la struttura delle
cartelle di output e le istruzioni per committare nel repo Dataform del progetto.

---

## Struttura cartelle output

```
projects/<DM_NAME>/
├── staging/
│   ├── <tabella_1>.sqlx
│   ├── <tabella_2>.sqlx
│   └── ...
├── public/
│   ├── <kpi_table>.sqlx
│   ├── <final_table>.sqlx
│   └── ...
└── README.md
```

`<DM_NAME>` è il nome del datamart in formato `DM_<NomeEntità>` (es. `DM_CustomerFidelity`).

---

## Formato SQLX — Regole obbligatorie

### Header commento
Ogni file `.sqlx` DEVE iniziare con un header commento:

```sql
-- ============================================================
-- Datamart  : <DM_NAME>
-- Layer     : Staging | Public
-- Tabella   : <nome_tabella>
-- Data      : <YYYY-MM-DD>
-- Requisito : <nome_file_requisito>
-- Descrizione: <descrizione breve della tabella>
-- Dipendenze:
--   <schema> : <tabella_1>
--            : <tabella_2>
-- ============================================================
```

### Config block
Il config block segue immediatamente l'header:

```sqlx
config {
  type: "table",            // "table" | "incremental" | "view" | "assertion"
  schema: "dm_<nome>",      // schema del datamart (es. "dm_customer_fidelity")
  name: "nome_tabella",     // snake_case, senza prefisso schema
  description: "Descrizione business della tabella.",
  tags: ["dm_<nome>", "staging"],   // sempre due tag: dm e layer

  // Solo per tabelle incrementali:
  // uniqueKey: ["customer_id"],

  // Partizionamento e clustering (solo se necessario):
  bigquery: {
    partitionBy: "DATE(subscription_date)",
    clusterBy: ["brand_code", "customer_code"]
  }
}
```

### Riferimenti a tabelle
Usa **sempre** `${ref()}` invece di nomi tabella hardcoded:

```sql
-- ✅ Corretto — schema + tabella
FROM ${ref("staging", "customer_fidelity_subscription")}

-- ✅ Corretto — stessa schema
FROM ${ref("customer_fidelity_subscription")}

-- ❌ Vietato — hardcoded
FROM `project.staging.customer_fidelity_subscription`
```

### Organizzazione SELECT
Raggruppa le colonne in sezioni commentate:

```sql
SELECT
  -- ================================================================
  -- SEZIONE 1: Chiavi identificative (HK)
  -- ================================================================
  S.customer_code                             AS customer_id,

  -- ================================================================
  -- SEZIONE 2: Dati subscription (HK)
  -- ================================================================
  S.subscription_platform_code               AS subscription_platform_id,

  -- ================================================================
  -- SEZIONE 3: KPI calcolati (BI)
  -- ================================================================
  ROUND(SUM(P.net_sales_eur), 2)             AS store_purchases_amount,

  -- Campo non disponibile a sistema (GAP documentato)
  CAST(NULL AS STRING)                        AS currency_code
```

---

## Esempio completo — tabella staging

```sqlx
-- ============================================================
-- Datamart  : DM_CustomerFidelity
-- Layer     : Staging
-- Tabella   : customer_fidelity_subscription
-- Data      : 2026-04-21
-- Requisito : Dem7685_Review_KPIs.pdf
-- Descrizione: Dati anagrafici di subscription per cliente/brand.
--              Arricchisce staging.customer_fidelity_subscription con
--              flag di loyalty e privacy.
-- Dipendenze:
--   staging : customer_fidelity_subscription
--           : loyalty_customer
--           : privacy_customer
-- ============================================================

config {
  type: "table",
  schema: "dm_customer_fidelity",
  name: "customer_fidelity_subscription",
  description: "Anagrafica subscription fidelity per cliente/brand, con flag loyalty e privacy.",
  tags: ["dm_customer_fidelity", "staging"],
  bigquery: {
    clusterBy: ["brand_code", "customer_code"]
  }
}

SELECT
  -- === Chiavi identificative (HK) ===
  CFS.customer_code,
  CAST(CFS.customer_fidelity_subscription_code AS STRING)  AS customer_fidelity_subscription_id,
  CFS.fidelity_code                                        AS fidelity_id,
  CFS.fidelity_card_code,

  -- === Dati subscription (HK) ===
  CFS.subscription_platform_code                           AS subscription_platform_id,
  CFS.platform_desc                                        AS subscription_platform_description,
  CFS.brand_code                                           AS subscription_brand_code,
  CFS.subscription_date,
  CFS.subscription_validity_end_date,
  CFS.unsubscription_date,

  -- === Flag loyalty (HK) ===
  LC.active_flag,
  LC.customer_contact_type_code,
  LC.signature_flag,
  LC.fidelity_subscripted_flag

FROM ${ref("staging", "customer_fidelity_subscription")} AS CFS

LEFT JOIN ${ref("staging", "loyalty_customer")} AS LC
  ON CFS.customer_code = LC.customer_code
  AND CFS.brand_code   = LC.brand_code
```

---

## Esempio completo — tabella staging con channel split

```sqlx
config {
  type: "table",
  schema: "dm_customer_fidelity",
  name: "customer_channel_purchases",
  description: "KPI acquisti per canale (store/online/cross) per customer/brand.",
  tags: ["dm_customer_fidelity", "staging"],
  bigquery: {
    clusterBy: ["brand_code", "customer_code"]
  }
}

WITH channel_agg AS (
  SELECT
    FS.customer_code,
    FS.customer_brand_code,
    ROUND(SUM(IF(FS.channel = 'offline', FS.net_sales_eur, 0)), 2)                 AS store_purchases_amount,
    SUM(IF(FS.channel = 'offline', FS.quantity, 0))                                AS store_purchases_pieces_number,
    COUNT(DISTINCT IF(FS.channel = 'offline', FS.document_code, NULL))             AS store_purchases_number,
    ROUND(SUM(IF(FS.channel IN ('eCommerce','app'), FS.net_sales_eur, 0)), 2)      AS online_purchases_amount,
    COUNT(DISTINCT IF(FS.channel IN ('eCommerce','app'), FS.document_code, NULL))  AS online_purchases_number
  FROM ${ref("staging", "full_sales")} AS FS
  GROUP BY FS.customer_code, FS.customer_brand_code
)

SELECT
  CA.customer_code,
  D_BRAND.brand_code,
  CA.store_purchases_amount,
  CA.store_purchases_pieces_number,
  CA.store_purchases_number,
  ROUND(SAFE_DIVIDE(CA.store_purchases_amount, NULLIF(CA.store_purchases_number, 0)), 2) AS store_average_purchase_amount,
  CA.online_purchases_amount,
  CA.online_purchases_number

FROM channel_agg AS CA
LEFT JOIN ${ref("normalised", "d_brand_c")} AS D_BRAND
  ON CA.customer_brand_code = D_BRAND.brand_id_code
```

---

## Istruzioni deployment su Dataform

Dopo aver generato i file localmente in `projects/<DM_NAME>/`:

1. Copia i file SQLX nel repo Dataform locale:
   ```
   definitions/<prefix>/staging/<tabella>.sqlx
   definitions/<prefix>/public/<tabella>.sqlx
   ```

2. Commit e push sul branch di sviluppo:
   ```powershell
   git checkout -b feat/<dm_name>
   git add definitions/<prefix>/
   git commit -m "feat(<dm_name>): add datamart SQLX files"
   git push origin feat/<dm_name>
   ```

3. Apri una Pull Request verso il branch `main` del repo Dataform.

4. Dopo merge, esegui una compilazione Dataform per validare i ref():
   ```bash
   dataform compile
   ```
