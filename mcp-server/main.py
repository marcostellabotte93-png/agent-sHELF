import os
import uvicorn
from fastmcp import FastMCP
from providers.factory import create_provider
from tools.list_agents import list_agents as _list_agents
from tools.get_agent import get_agent as _get_agent
from tools.get_skill import get_skill as _get_skill

mcp = FastMCP("agent-shelf")
provider = create_provider()


@mcp.tool()
async def list_agents() -> str:
    """
    Lista tutti gli agenti disponibili nella libreria agent-shelf.
    Restituisce un array JSON con metadati (id, name, version, category, description, author).
    Non include il contenuto dei system prompt o delle skills.
    """
    return await _list_agents(provider)


@mcp.tool()
async def get_agent(id: str) -> str:
    """
    Scarica e restituisce un agente completo dalla libreria.

    Restituisce un oggetto JSON con:
    - system_prompt: contenuto delle skills core concatenate (da iniettare nel contesto)
    - available_skills: lista delle skills extended disponibili on-demand
    - mcp_servers: configurazione dei server MCP esterni necessari
    - metadata: id, name, version, category

    Il chiamante deve usare system_prompt come system prompt della sessione.

    Se vscode_mcp_config non è null, seguire questo processo differenziato per tipo:

    SERVER HTTP (type: http) — configurazione dinamica nel workspace corrente:
    1. Scrivere vscode_mcp_config nel file .vscode/mcp.json della cartella di lavoro
       corrente (crearla se non esiste). VS Code la rileva automaticamente.
    2. Se il blocco contiene inputs con "password": true, VS Code chiederà
       il valore al primo utilizzo e lo salverà nel keychain del SO.
    3. Comunicare all'utente: "Ho aggiunto la configurazione MCP in .vscode/mcp.json.
       Esegui 'MCP: List Servers' dal Command Palette per attivarla."
    4. Attendere conferma dell'utente prima di procedere con la sessione.

    SERVER STDIO (type: stdio o assente) — configurazione manuale:
    1. Mostrare il blocco server estratto da vscode_mcp_config
    2. Istruire l'utente ad aggiungerlo a ~/.vscode/mcp.json (NON a .vscode/ del workspace)
    3. Chiedere i valori delle variabili env_required (non mostrarle nei log)
    4. Chiedere all'utente di ricaricare i server MCP
    I valori in env_optional hanno un default e non bloccano l'avvio.
    """
    return await _get_agent(provider, id)


@mcp.tool()
async def get_skill(agent_id: str, skill_name: str) -> str:
    """
    Carica una skill extended on-demand per un agente attivo.

    Usare questo tool quando durante la sessione emerge la necessità
    di una competenza specifica non inclusa nel system prompt iniziale.

    skill_name è il nome del file senza path e senza .md
    (es. 'python-review' per 'skills/python-review.md').
    """
    return await _get_skill(provider, agent_id, skill_name)


# ASGI app esposta per uvicorn: `uvicorn main:app --host 0.0.0.0 --port 8000`
# L'endpoint MCP è disponibile su http://host:port/mcp (streamable-http)
app = mcp.get_asgi_app()


def run():
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        log_level="info",
    )


if __name__ == "__main__":
    run()
