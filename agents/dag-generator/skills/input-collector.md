# Skill: Input Collector

Purpose: guidare la raccolta delle informazioni minime necessarie alla creazione
di un DAG, facendo poche domande mirate e adattive in base al tipo selezionato.

---

## Obiettivo

Questa skill separa la fase di intervista dalla fase di generazione. Deve
ridurre al minimo il numero di domande, evitando sia richieste ridondanti sia
generazione con dati incompleti.

---

## Flusso

### 1. Identifica il tipo DAG

Se non è già noto, chiedi:
- `Che DAG devi creare: cdf, cf o df?`

Se la risposta è `df`, chiedi:
- `È un DAG df_bronze o df_semantic?`

### 2. Costruisci la scheda input

Raccogli sempre una scheda strutturata con i campi noti e quelli ancora mancanti.
Formato suggerito:

| Campo | Valore |
|---|---|
| `dag_type` | |
| `subtype` | |
| `domain` | |
| `dag_id` | |
| `asset_name` | |
| `target_folder` | |
| `schedule_interval` | |

Poi aggiungi i campi specifici del tipo DAG.

### 3. Domande specifiche per `cdf`

Chiedi solo se non deducibili dai template o da esempi simili:
- descrizione breve
- `namespace`
- nome file config
- `version`
- runtime args obbligatori

### 4. Domande specifiche per `cf`

Chiedi solo se non deducibili:
- descrizione breve
- URL Cloud Function per ambiente o pattern di derivazione
- metodo HTTP
- autenticazione IAM sì/no
- payload richiesto
- headers richiesti

### 5. Domande specifiche per `df`

Chiedi solo se non deducibili:
- descrizione breve
- `SOURCE_TABLE`
- `DESTINATION_TABLE`
- `REPOSITORY_ID`
- `DF_TAGS` o target file
- DAG upstream da triggerare

---

## Regole

- Non fare tutte le domande in blocco se il template o esempi vicini permettono
  di dedurre parte dei valori.
- Se l'utente fornisce un esempio di DAG simile, usalo come sorgente primaria
  per naming e cartella target.
- Prima di passare alla generazione, ricapitola la scheda input e segnala i
  campi ancora mancanti o assunti.