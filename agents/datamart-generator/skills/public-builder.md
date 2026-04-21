# Skill: Public Builder

Purpose: progettare e generare le tabelle public del datamart come file SQLX
Dataform, incluso il calcolo dei KPI e la tabella finale consolidata.

---

## Principi delle tabelle public

Le tabelle public:
- **Aggregano** dati dalle tabelle staging DM o dalle staging/public esistenti
- **Calcolano KPI** business (da SQLX esistenti o inferiti dal requisito)
- **Espongono** il grain corretto (es. una riga per customer/brand)
- Sono la fonte diretta per Marketing Cloud e altri sistemi downstream
- Hanno sempre `schema: "dm_<nome_datamart>"` nel config block

---

## Struttura SQLX public — tabella finale consolidata

La tabella finale unisce tutti i KPI in un'unica riga per chiave primaria.
Usa sempre `LEFT JOIN` per preservare tutti i customer dalla tabella base.

```sqlx
config {
  type: "table",
  schema: "dm_<nome_datamart>",
  name: "<dm_name>_final",
  description: "Tabella finale consolidata — tutti i campi del requisito",
  tags: ["dm_<nome_datamart>", "public", "final"],
  uniqueKey: ["<chiave_primaria>"],
  bigquery: {
    partitionBy: "<campo_data_tecnico>",
    clusterBy: ["<campo_brand>"]
  }
}

SELECT
  -- ================================================================
  -- SEZIONE 1: Chiavi identificative (HK)
  -- ================================================================
  BASE.<chiave_1>                                     AS <nome_requisito>,
  BASE.<chiave_2>                                     AS <nome_requisito>,

  -- ================================================================
  -- SEZIONE 2: Campi sorgente diretti (HK)
  -- ================================================================
  BASE.<campo_hk>,

  -- ================================================================
  -- SEZIONE 3: KPI calcolati (BI)
  -- ================================================================
  KPI.<kpi_amount>                                    AS <nome_requisito>,
  KPI.<kpi_count>                                     AS <nome_requisito>,
  ROUND(SAFE_DIVIDE(KPI.<kpi_amount>, KPI.<kpi_count>), 2) AS <avg_requisito>,

  -- Campo non disponibile a sistema (GAP documentato)
  CAST(NULL AS STRING)                                AS <campo_gap>,

  -- Metadato tecnico
  CURRENT_DATE()                                      AS last_update_date

FROM ${ref("dm_<nome_datamart>", "<tabella_base>")} AS BASE

LEFT JOIN ${ref("dm_<nome_datamart>", "<kpi_staging>")} AS KPI
  ON BASE.<chiave> = KPI.<chiave>
  AND BASE.<brand> = KPI.<brand>

LEFT JOIN ${ref("public", "<tabella_public_esistente>")} AS PUB
  ON BASE.<chiave> = PUB.<chiave>
```

---

## Logica KPI dal requisito

### Campi `defined_by: HK` (sistema sorgente)
→ Seleziona direttamente dalla staging senza calcoli.

### Campi `defined_by: BI` (calcolati)
Applica questa priorità per la logica di calcolo:

1. **SQLX disponibile** nel documenter → copia la formula esatta dal `sql_text`
2. **Nome semanticamente chiaro** → inferisci la formula standard:
   - `*_amount` → `ROUND(SUM(...), 2)`
   - `*_pieces_number` / `*_number` → `SUM(quantity)` o `COUNT(DISTINCT document_code)`
   - `*_average_*` → `ROUND(SAFE_DIVIDE(SUM(), COUNT(DISTINCT ...)), 2)`
   - `last_*_date` → `MAX()` con `QUALIFY ROW_NUMBER() = 1`
   - `favourite_*` → sottoquery con `QUALIFY ROW_NUMBER() OVER (ORDER BY COUNT DESC) = 1`
3. **Formula non deducibile** → `CAST(NULL AS <tipo>) AS <campo>` con commento `-- TODO: formula da validare con business`

### Pattern KPI comuni

```sql
-- Importo totale per canale (store/online)
ROUND(SUM(IF(channel = 'offline', net_sales_eur, 0)), 2)     AS store_purchases_amount
ROUND(SUM(IF(channel IN ('eCommerce','app'), net_sales_eur, 0)), 2) AS online_purchases_amount

-- Pezzi per canale
SUM(IF(channel = 'offline', quantity, 0))                     AS store_purchases_pieces_number

-- Numero documenti per canale
COUNT(DISTINCT IF(channel = 'offline', document_code, NULL))  AS store_purchases_number

-- Ticket medio
ROUND(SAFE_DIVIDE(store_purchases_amount, NULLIF(store_purchases_number, 0)), 2) AS store_average_purchase_amount

-- Store preferito (più acquisti)
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY customer_code, brand_code
  ORDER BY COUNT(DISTINCT document_code) DESC
) = 1

-- Last/secondlast purchase
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY customer_code, brand_code
  ORDER BY document_date DESC
) = 1   -- last
-- ) = 2   -- secondlast

-- Canale OTP da customer_contact_type_code
CASE
  WHEN customer_contact_type_code = 1                 THEN 'eMail'
  WHEN customer_contact_type_code = 2                 THEN 'Telefono Mobile'
  WHEN customer_contact_type_code IS NULL
   AND signature_flag = 1                             THEN 'Signature'
  ELSE NULL
END                                                   AS loyalty_subscript_otp_channel
```

---

## Copertura requisito

Prima di generare, costruisci questa matrice di validazione:

| required_field | covered_by_table | covered_by_column | formula_source | status |
|---|---|---|---|---|
| `customer_id` | staging.customer_base | customer_code | direct | ✅ ok |
| `store_purchases_amount` | staging.channel_purchases | store_purchases_amount | inferred | ⚠️ validare |
| `currency_code` | — | — | — | ❌ gap |

Presenta questa matrice all'utente prima di finalizzare i file.

---

## Checklist tabella final

- [ ] Ogni campo del requisito con `in_current_flow: YES` è presente
- [ ] Ogni KPI `defined_by: BI` ha una formula (anche con TODO se non certa)
- [ ] `LEFT JOIN` usato per preservare tutti i customer (no INNER JOIN sulla tabella finale)
- [ ] I GAP sono documentati come `CAST(NULL AS <tipo>) AS <campo>` con commento
- [ ] `uniqueKey` dichiarato nel config se la tabella è idempotente
- [ ] Nessun `SELECT *` nella tabella final
- [ ] `${ref()}` per tutti i riferimenti a tabelle
