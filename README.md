# agent-shelf

Libreria centralizzata di agenti AI aziendali. Ogni agente è composto da un system prompt, skills opzionali e configurazione di eventuali MCP server esterni.

Un server MCP locale legge questa repository via GitHub API e la espone come tool calls a VS Code / GitHub Copilot Agent Mode.

```
Copilot Agent Mode  ←→  MCP Server (locale)  ←→  GitHub API  ←→  agent-shelf repo
```

## Tool calls disponibili

| Tool | Descrizione |
|---|---|
| `list_agents` | Lista tutti gli agenti con metadati (id, nome, categoria, descrizione) |
| `get_agent` | Restituisce system prompt + skills + config MCP per un agente specifico |
| `get_skill` | Carica una skill extended on-demand durante una sessione attiva |

## Agenti disponibili

| ID | Nome | Categoria | Descrizione |
|----|------|-----------|-------------|
| `code-reviewer` | Code Reviewer | engineering | Revisione codice con focus su qualità, sicurezza e best practice |
| `looker-analyst` | Looker Analyst | analytics | Analisi dati su Looker con focus su metriche business |
| `notion-writer` | Notion Writer | writing | Creazione e aggiornamento di pagine Notion con struttura coerente |

## Struttura della repository

```
agents/
└── <agent-id>/
    ├── agent.json          # metadati e manifest delle skills
    ├── system-prompt.md    # istruzioni principali (sempre caricate)
    └── skills/
        └── <skill>.md     # conoscenza specializzata (caricata on-demand)

mcp-server/
├── main.py                 # entry point FastMCP
├── pyproject.toml
├── providers/              # adapter per provider Git
│   ├── base.py
│   ├── github.py
│   └── factory.py
└── tools/                  # logica tool calls separata in moduli
    ├── list_agents.py
    ├── get_agent.py
    └── get_skill.py
```

## Setup del MCP Server

### Prerequisiti

- Docker (opzione consigliata) oppure Python 3.11+
- GitHub Personal Access Token con scope `Contents: Read` (fine-grained) o `repo` (classic)

---

### Opzione A — Docker (consigliata)

Il server espone un endpoint HTTP su porta 8000 gestito da **uvicorn**.

#### 1. Build dell'immagine

```bash
cd mcp-server
docker build -t agent-shelf-mcp:latest .
```

#### 2. Avvio del container

```bash
docker run -d --name agent-shelf \
  -p 8000:8000 \
  -e GIT_PROVIDER=github \
  -e GITHUB_TOKEN=ghp_... \
  -e GITHUB_OWNER=nome-organizzazione \
  -e GITHUB_REPO=agent-shelf \
  -e GITHUB_BRANCH=main \
  agent-shelf-mcp:latest
```

Porta e host personalizzabili via variabili d'ambiente: `-e PORT=9000 -e HOST=127.0.0.1`.

#### 3. Configurazione VS Code

Aggiungi al tuo file `~/.vscode/mcp.json` (crealo se non esiste):

```json
{
  "servers": {
    "agent-shelf": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

Nessun token in questo file: le credenziali GitHub vivono nel container, non nel client.

#### 4. Test con MCP Inspector via Docker

```bash
npx @modelcontextprotocol/inspector http://localhost:8000/mcp
```

---

### Opzione B — Python diretto

#### 1. Installazione

```bash
cd mcp-server
pip install -e .
```

#### 2. Configurazione VS Code

Aggiungi al tuo file `~/.vscode/mcp.json`:

```json
{
  "servers": {
    "agent-shelf": {
      "command": "python",
      "args": ["-m", "main"],
      "cwd": "/percorso/assoluto/a/agent-shelf/mcp-server",
      "env": {
        "GIT_PROVIDER": "github",
        "GITHUB_TOKEN": "${input:githubToken}",
        "GITHUB_OWNER": "nome-organizzazione",
        "GITHUB_REPO": "agent-shelf",
        "GITHUB_BRANCH": "main"
      }
    }
  },
  "inputs": [
    {
      "id": "githubToken",
      "type": "promptString",
      "description": "GitHub Personal Access Token (scope: contents:read)",
      "password": true
    }
  ]
}
```

Sostituisci `/percorso/assoluto/a/agent-shelf/mcp-server` con il path reale.

#### 3. Test con MCP Inspector

```bash
cd mcp-server
npx @modelcontextprotocol/inspector python -m main
```

### Variabili d'ambiente

| Variabile | Richiesta | Default | Descrizione |
|-----------|-----------|---------|-------------|
| `GIT_PROVIDER` | No | `github` | Provider Git (attualmente: `github`) |
| `GITHUB_TOKEN` | Sì | — | Personal Access Token |
| `GITHUB_OWNER` | Sì | — | Username o organizzazione GitHub |
| `GITHUB_REPO` | Sì | — | Nome della repository |
| `GITHUB_BRANCH` | No | `main` | Branch da leggere |

## Aggiungere un nuovo agente

1. Crea la cartella `agents/<agent-id>/` — l'ID deve corrispondere esattamente al nome cartella
2. Scrivi `agent.json` seguendo lo schema (vedi agenti esistenti come riferimento)
3. Scrivi `system-prompt.md` con le istruzioni principali dell'agente
4. Aggiungi le skills in `skills/<nome>.md` e referenziale in `agent.json`
5. Apri una Pull Request — la GitHub Action validerà automaticamente la struttura prima del merge
