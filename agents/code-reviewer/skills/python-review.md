# Python Code Review Guidelines

## Stile e convenzioni

- Segui PEP 8 e PEP 20 (The Zen of Python)
- Usa type hints (PEP 484) per tutte le funzioni pubbliche; preferisci `X | None` a `Optional[X]` su Python 3.10+
- Preferisci f-string alle concatenazioni con `+` e a `.format()` per leggibilità
- Usa `pathlib.Path` invece di `os.path` per operazioni sul file system

## Pattern da segnalare come problemi

### Gestione eccezioni
- `except Exception:` senza re-raise o logging adeguato — specificare sempre il tipo di eccezione
- Blocchi `except` vuoti o con solo `pass` — mascherano errori silenziosamente
- Uso di `sys.exit()` dentro funzioni non-main — lancia eccezioni, non esci brutalmente

### Argomenti di default mutabili
```python
# Problematico — la lista è condivisa tra tutte le chiamate
def aggiungi(elemento, lista=[]):
    lista.append(elemento)
    return lista

# Corretto
def aggiungi(elemento, lista=None):
    if lista is None:
        lista = []
    lista.append(elemento)
    return lista
```

### Altri anti-pattern
- Import circolari — segnala e suggerisci refactor con dependency injection o lazy import
- Uso di `global` e `nonlocal` senza necessità — favorire il passaggio esplicito di stato
- List comprehension annidate su più livelli: difficile da leggere, meglio ciclo esplicito con nome descrittivo
- Confronto con `True`/`False`/`None` con `==` invece di `is` / `is not`

## Pattern consigliati

- Context manager (`with`) per tutte le risorse: file, connessioni DB, lock, sessioni HTTP
- `dataclass` o Pydantic `BaseModel` per strutture dati invece di dizionari ad-hoc
- `@property` e `@cached_property` per attributi computati che non devono essere chiamati come metodi
- Generator e `yield` per sequenze potenzialmente grandi — evita di materializzare liste inutili
- `abc.ABC` con `@abstractmethod` per interfacce — garantisce che le sottoclassi implementino i contratti

## Async Python

- Non inserire codice sync bloccante in coroutine async: `time.sleep` → `asyncio.sleep`, operazioni I/O sync → versioni async
- Usa `asyncio.gather()` per lanciare operazioni I/O in parallelo invece di attendere sequenzialmente
- Non creare task senza gestire il loro ciclo di vita — usa `asyncio.TaskGroup` (Python 3.11+) quando possibile
- Attenzione a condivisione di stato mutabile tra coroutine concorrenti: usa `asyncio.Lock` se necessario

## Testing

- Ogni funzione pubblica deve avere almeno un test che copra il caso nominale e uno il caso di errore
- Usa `pytest.fixture` per setup condivisi tra test — evita duplicazione nel setup
- Mocking: `unittest.mock.patch` o `pytest-mock` per isolare dipendenze esterne
- Controlla sempre i casi limite: `None`, lista vuota, stringa vuota, valori al boundary numerico
- I test non devono dipendere dall'ordine di esecuzione — ogni test deve essere autonomo
