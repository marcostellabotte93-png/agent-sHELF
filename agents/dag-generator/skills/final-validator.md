# Skill: Final Validator

Purpose: verificare che il DAG generato sia coerente con il repository, completo
nei parametri e formattato come i template vicini, includendo controllo finale
su blank lines e placeholder residui.

---

## Controlli obbligatori

### 1. Coerenza strutturale

Verifica:
- file creato nella cartella corretta
- naming del file coerente con il `dag_id`
- eventuale config YAML nella cartella prevista
- import delle `utils` corretto per il tipo DAG scelto

### 2. Coerenza semantica

Verifica:
- tutte le costanti obbligatorie valorizzate
- nessun placeholder residuo (`your_`, `TODO`, `Replace`, `YOUR_`)
- `tags` coerenti con il dominio e con i DAG vicini
- upstream corretti (`cdf`, `cf`, `df`) in base allo scenario

### 3. Coerenza con i template locali

Confronta con il template sorgente e con almeno un DAG vicino dello stesso
tipo. Controlla:
- ordine delle costanti
- stile commenti
- struttura `default_args`
- blocco `with DAG(...)`
- costruzione della dependency chain finale

### 4. Formattazione e blank lines

Verifica esplicitamente:
- singola blank line tra import group e definizioni successive
- nessuna doppia blank line non giustificata
- spaziatura coerente dentro liste e dict
- allineamento generale uguale ai template adiacenti

Se il repository usa formatter o linter noti, esegui il controllo più stretto
disponibile. Se non esistono tool automatici, fai almeno validazione visiva
comparativa contro il template di riferimento.

---

## Output finale da produrre

Restituisci sempre un riepilogo con:

| Sezione | Contenuto |
|---|---|
| `files_created` | elenco path dei file creati |
| `files_updated` | elenco path dei file modificati |
| `validation_checks` | controlli eseguiti |
| `open_assumptions` | eventuali ipotesi ancora non confermate |
| `ready_for_use` | yes/no |

Se manca un'informazione e il file non è affidabile, `ready_for_use` deve essere
`no`.