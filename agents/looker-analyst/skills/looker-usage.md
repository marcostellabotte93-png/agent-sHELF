# Looker MCP Server — Guida all'uso dei tool

Questa skill descrive come usare i tool del server MCP Looker durante una sessione attiva. Caricala quando devi interagire direttamente con i dati Looker tramite i tool calls.

## Prerequisiti

Il server MCP Looker gira come container Docker (`looker-mcp-toolbox`) e viene avviato da VS Code tramite la configurazione in `.vscode/mcp.json`.

Variabili richieste (VS Code le chiede via input box alla prima attivazione):
- `LOOKER_CLIENT_ID`: Client ID delle API Looker
- `LOOKER_CLIENT_SECRET`: Client Secret delle API Looker

Variabili con default aziendale (non richiedono inserimento):
- `LOOKER_BASE_URL`: `https://jakala.cloud.looker.com/`
- `LOOKER_VERIFY_SSL`: `true`

## Tool disponibili

### `looker_run_query`
Esegue una query su un Explore di Looker e restituisce i risultati come array di oggetti.

**Parametri:**
- `model` (string): nome del modello LookML (es. `ecommerce`, `marketing`)
- `explore` (string): nome dell'Explore (es. `orders`, `sessions`)
- `fields` (array): campi nel formato `view_name.field_name` (es. `["orders.count", "orders.created_month"]`)
- `filters` (object): filtri come coppie chiave-valore (es. `{"orders.status": "complete", "orders.created_date": "last 30 days"}`)
- `sorts` (array, opzionale): ordinamento (es. `["orders.created_month desc"]`)
- `limit` (number, opzionale): max righe restituite, default 500

**Esempio:**
```json
{
  "model": "ecommerce",
  "explore": "orders",
  "fields": ["orders.created_month", "orders.total_revenue", "orders.count"],
  "filters": {"orders.status": "complete", "orders.created_date": "last 12 months"},
  "sorts": ["orders.created_month desc"],
  "limit": 24
}
```

### `looker_get_explores`
Lista tutti gli Explore disponibili in un modello con la loro descrizione.

**Parametri:**
- `model` (string): nome del modello

### `looker_get_fields`
Restituisce dimensioni e misure disponibili per un Explore specifico, con tipo e descrizione.

**Parametri:**
- `model` (string): nome del modello
- `explore` (string): nome dell'Explore

### `looker_get_looks`
Lista i Look (report salvati) accessibili all'utente corrente, con ID e titolo.

### `looker_run_look`
Esegue un Look esistente e ne restituisce i dati aggiornati.

**Parametri:**
- `look_id` (number): ID del Look da eseguire

## Workflow consigliato

1. **Scoperta**: usa `looker_get_explores` per identificare il modello e l'Explore corretto
2. **Campi**: usa `looker_get_fields` per scoprire dimensioni e misure disponibili
3. **Query**: costruisci e lancia la query con `looker_run_query`
4. **Iterazione**: se i dati non corrispondono alle aspettative, verifica filtri e tipi di campo

## Gestione dei tipi di campo

- **Dimensioni** (`dimension`): attributi descrittivi — categorie, date, ID, testi. Usabili in `fields` e `filters`
- **Misure** (`measure`): aggregazioni calcolate — count, sum, average, ecc. Usabili in `fields`, **non direttamente in `filters`**
- **Dimension group**: dimensioni temporali con granularità multiple — specifica sempre la granularità: `created_date`, `created_month`, `created_year`, `created_week`

## Sintassi dei filtri temporali

| Espressione | Significato |
|---|---|
| `"last 30 days"` | ultimi 30 giorni da oggi |
| `"last 3 months"` | ultimi 3 mesi |
| `"this month"` | mese corrente |
| `"2025/01/01 to 2025/12/31"` | range data esplicito |
| `"before 2025/01/01"` | prima di una data |
