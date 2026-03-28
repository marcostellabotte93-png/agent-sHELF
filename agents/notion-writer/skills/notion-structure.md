# Notion — Template strutturali per tipo di documento

Usa questa skill quando devi creare un documento specifico. Scegli il template corrispondente e adattalo al contesto.

---

## Pagina Progetto

```
# [Nome Progetto]

> 💡  [Una frase che descrive lo scopo e il perché del progetto]

| Campo    | Valore                        |
|----------|-------------------------------|
| Owner    | @nome                         |
| Stato    | 🟡 In corso                   |
| Deadline | YYYY-MM-DD                    |
| Team     | @persona1, @persona2          |

---

## Obiettivi
- Obiettivo principale 1
- Obiettivo principale 2

## Scope
### In scope
- ...
### Out of scope
- ...

## Decisioni chiave
| Data       | Decisione       | Motivazione     | Owner |
|------------|-----------------|-----------------|-------|
| YYYY-MM-DD | ...             | ...             | @nome |

## Rischi
| Rischio | Probabilità | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| ...     | Alta        | Alto    | ...         |

## Link utili
- [Documento correlato](#)
- [Ticket tracker](#)
```

---

## Meeting Notes

```
# Meeting — [Titolo] — YYYY-MM-DD

**Partecipanti**: @nome1, @nome2, @nome3
**Durata**: XX min
**Recording**: [link se disponibile]

---

## Agenda
1. Punto 1
2. Punto 2

## Note e decisioni

### [Punto 1 — titolo]
- Contesto discussione
- ✅ **Decisione**: descrizione della decisione presa

### [Punto 2 — titolo]
- ...

## Action items
| Task | Owner | Deadline | Stato |
|------|-------|----------|-------|
| ... | @nome | YYYY-MM-DD | ⬜ |
| ... | @nome | YYYY-MM-DD | ⬜ |

## Prossimo meeting
Data: / Link:
```

---

## ADR (Architecture Decision Record)

```
# ADR-[NNN] — [Titolo della decisione]

**Data**: YYYY-MM-DD
**Stato**: Proposta | Accettata | Deprecata | Sostituita da ADR-XXX
**Deciders**: @nome1, @nome2

---

## Contesto
[Descrizione del problema o della situazione che richiede una decisione.
Cosa ci ha spinto a dover scegliere?]

## Opzioni considerate

### Opzione A — [nome breve]
- Pro: ...
- Contro: ...

### Opzione B — [nome breve]
- Pro: ...
- Contro: ...

## Decisione
**Scelta: Opzione A**

Motivazione: [perché questa opzione rispetto alle altre]

## Conseguenze
### Positive
- ...

### Negative / Trade-off
- ...

## Note
[Riferimenti, link a ticket, documenti correlati]
```

---

## Runbook operativo

```
# Runbook — [Nome procedura]

> ⚠️ **Prerequisiti**: [cosa serve prima di iniziare — accessi, tool, permessi]

**Tempo stimato**: X minuti
**Frequenza**: giornaliera | settimanale | mensile | on-demand
**Owner**: @nome — contattare su #canale-slack per problemi

---

## Steps

### 1. [Titolo step]
Descrizione breve di cosa fa questo step.

```bash
comando-esempio --flag parametro
```

✅ **Verifica**: cosa aspettarsi come output se lo step è andato a buon fine

---

### 2. [Titolo step]
...

---

## Troubleshooting
| Sintomo | Causa probabile | Soluzione |
|---------|-----------------|-----------|
| Errore X | Permessi mancanti | Verificare ruolo IAM Y |

## Escalation
Contattare @nome su #canale-slack oppure aprire un ticket su [link].
```

---

## Convenzioni generali

- **Stato del documento**: sempre visibile in cima — usa le emoji: 🟢 Pubblicato, 🟡 In revisione, 🔴 Bozza, ⚫ Archiviato
- **Date**: sempre nel formato `YYYY-MM-DD` per ordinamento corretto nei database
- **Callout**: `> ⚠️` per warning critici, `> 💡` per note informative, `> ✅` per conferme di successo
- **Toggle**: usa i toggle Notion per sezioni lunghe o tecniche che non tutti devono leggere immediatamente
- **Database**: configura sempre almeno le proprietà `Status`, `Owner` e `Ultima modifica (auto)`
