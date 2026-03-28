# Security Audit Guidelines

Questa skill guida un audit di sicurezza approfondito basato sull'OWASP Top 10. Usala quando viene richiesta una revisione con focus esplicito sulla sicurezza o quando il codice tratta autenticazione, autorizzazione, input utente o dati sensibili.

## Classificazione della severità

Per ogni vulnerabilità trovata, classifica usando:
- **CRITICO**: sfruttabile da remoto senza autenticazione, impatto su confidenzialità/integrità/disponibilità
- **ALTO**: sfruttabile con accesso autenticato o richiede interazione utente, impatto significativo
- **MEDIO**: difficile da sfruttare o impatto limitato, ma da correggere
- **BASSO**: configurazione migliorabile, difesa in profondità
- **INFORMATIVO**: best practice da considerare, nessun rischio immediato

## OWASP Top 10 — checklist di revisione

### A01 — Broken Access Control
- Ogni endpoint/funzione controlla i permessi dell'utente prima di eseguire l'azione?
- Cerca IDOR (Insecure Direct Object Reference): accesso a risorse tramite ID numerico senza verifica ownership
- Le route amministrative sono protette da middleware di autenticazione/autorizzazione?
- I controlli di autorizzazione sono lato server, non solo lato client

### A02 — Cryptographic Failures
- **CRITICO**: chiavi, token o password hardcoded nel codice sorgente
- Non usare MD5 o SHA-1 per hashing di password → usa bcrypt, argon2 o PBKDF2 con salt adeguato
- Verifica che dati sensibili non vengano loggati (password, token, PII)
- Connessioni HTTP non cifrate per dati sensibili → segnalare come ALTO
- Cerca pattern `verify=False`, `ssl._create_unverified_context()` o equivalenti

### A03 — Injection
- **SQL injection**: concatenazione diretta di input utente nelle query → parameterized queries obbligatorie
```python
# Vulnerabile
query = f"SELECT * FROM users WHERE name = '{user_input}'"
# Corretto
query = "SELECT * FROM users WHERE name = %s"
cursor.execute(query, (user_input,))
```
- **Command injection**: `subprocess` con `shell=True` + input non sanitizzato → CRITICO; usa `shell=False` con lista di argomenti
- **Template injection**: input utente passato direttamente a `render_template_string()` o equivalenti

### A04 — Insecure Design
- La logica business critica (es. sconti, quantità ordini, prezzi) viene validata lato server?
- Le operazioni distruttive (delete, revoke) richiedono conferma esplicita?

### A05 — Security Misconfiguration
- Debug mode attivo in produzione: `DEBUG=True`, `app.debug = True`, stack trace esposto agli utenti
- CORS wildcard (`Access-Control-Allow-Origin: *`) su API che espongono dati autenticati
- Secret management: variabili d'ambiente vs. file di configurazione committati in repo
- Header di sicurezza HTTP assenti: `Strict-Transport-Security`, `X-Content-Type-Options`, `Content-Security-Policy`

### A07 — Identification and Authentication Failures
- Token/session ID non invalidati al logout o alla scadenza
- Assenza di rate limiting su endpoint di login, reset password, OTP
- JWT: verifica che l'algoritmo sia validato (`alg: none` attack) e che il secret sia robusto

### A08 — Software and Data Integrity Failures
- Dipendenze installate senza verifica di integrità (checksum, lock file)
- Deserializzazione di input non fidato (pickle, yaml.load senza SafeLoader)

### A09 — Security Logging and Monitoring Failures
- Gli eventi di sicurezza vengono loggati? (login falliti, accessi negati, operazioni privilegiate)
- I log contengono dati sensibili (password, token, numeri di carta)?
- È presente un meccanismo di alerting per anomalie?

## Come riportare una vulnerabilità

Usa sempre questo formato:

```
**[SEVERITÀ] Titolo del problema**
- Posizione: file.py, riga N / funzione `nome_funzione`
- Descrizione: cosa succede e perché è un problema
- Vettore di attacco: come potrebbe essere sfruttato
- Fix consigliato: [snippet di codice corretto]
```
