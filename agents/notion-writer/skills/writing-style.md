# Guida allo Stile di Scrittura Aziendale

Questa skill definisce le convenzioni di stile, tono e formato per tutta la produzione documentale su Notion.

## Principi fondamentali

### 1. Chiarezza prima dell'eleganza
- Frasi brevi: idealmente sotto le 20 parole per frase
- Una frase = un'informazione — non comprimere due concetti in una frase con "e"
- Evita il nominalismo: preferisci "decidiamo" a "procediamo alla presa di decisione"

### 2. Voce attiva
- ✅ "Il team ha rilasciato la feature in produzione"
- ❌ "La feature è stata rilasciata in produzione dal team"
- Eccezione: la voce passiva è accettabile per procedure dove l'agente non è rilevante ("Il file viene elaborato automaticamente")

### 3. Consistenza terminologica
- Definisci i termini chiave alla prima occorrenza e usali sempre allo stesso modo
- Non alternare sinonimi per varietà stilistica — in documenti tecnici crea confusione
- Esempio: se scegli "utente", non alternare con "cliente", "account", "user" nello stesso documento

### 4. Concisione
- Ogni parola deve guadagnarsi il proprio posto
- Elimina frasi di riscaldamento: "In questa sezione tratteremo...", "Come vedremo di seguito..."
- Riduci gli avverbi intensificatori: "molto importante" → "critico"

---

## Tono per contesto

### Documentazione tecnica (Engineering / Data)
- **Tono**: preciso, diretto, neutro
- Usa termini tecnici senza spiegazioni se il pubblico è tecnico per definizione
- Esempi di codice sempre in blocchi formattati con lingua specificata
- Definisci acronimi alla prima occorrenza: `MTTR (Mean Time to Resolve)`
- Evita opinioni non motivate — scrivi "preferire X perché Y" non solo "è meglio X"

### Documentazione operativa (Operations / HR / Finance)
- **Tono**: chiaro, accessibile, action-oriented
- Evita jargon tecnico — se necessario, aggiungi una nota esplicativa tra parentesi
- Liste numerate per procedure sequenziali, liste puntate per opzioni/elementi non ordinati
- Ogni step deve essere verificabile: "Clicca su X" → poi "Verifica che appaia Y"

### Comunicazioni di prodotto (Stakeholder business)
- **Tono**: fiducioso, orientato ai benefici, conciso
- Struttura standard: **Contesto** → **Impatto** → **Prossimi passi**
- Quantifica sempre quando possibile: "riduce il tempo di X del 40%" > "migliora significativamente X"
- Evita dettagli implementativi a meno che non siano esplicitamente richiesti

---

## Struttura raccomandata per ogni documento

1. **Titolo**: cosa è il documento, per chi è — senza ambiguità
2. **TL;DR / Sommario**: max 3 righe con l'essenziale — anche chi non legge il resto deve capire il punto
3. **Corpo**: informazione strutturata in sezioni con intestazioni descrittive
4. **Action items / Next steps**: sempre espliciti con owner e deadline — mai lasciare il documento senza un "quindi cosa facciamo"

---

## Checklist pre-pubblicazione

- [ ] Il titolo descrive il contenuto senza ambiguità
- [ ] C'è un owner identificato (persona specifica, non "il team")
- [ ] Le date sono nel formato `YYYY-MM-DD`
- [ ] I link sono tutti funzionanti
- [ ] Lo stato del documento è aggiornato (Bozza / In revisione / Approvato / Archiviato)
- [ ] Le menzioni `@persona` sono corrette e le persone menzionate hanno accesso alla pagina
- [ ] Gli action item hanno tutti un owner e una deadline
- [ ] Non ci sono informazioni sensibili (credenziali, dati personali) in pagine ad accesso allargato

---

## Termini da evitare

| Da evitare | Alternativa |
|---|---|
| "sfruttare" (leverage) | "usare", "applicare" |
| "sinergizzare" | "collaborare", "integrare" |
| "a livello di" | "per", "in" |
| "in termini di" | specifica il termine |
| "come detto in precedenza" | ripeti il concetto o linka la sezione |
| "ASAP" | specifica la data |
