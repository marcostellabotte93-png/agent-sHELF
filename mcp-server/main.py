import os
import uvicorn
from fastmcp import FastMCP
from providers.factory import create_provider
from tools.list_agents import list_agents as _list_agents
from tools.get_agent import get_agent as _get_agent
from tools.get_skill import get_skill as _get_skill
from tools.configure_workspace import configure_workspace as _configure_workspace

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

    SERVER STDIO (type: stdio o assente) — configurazione automatica:
    1. Chiedere all'utente il path della cartella di lavoro corrente (workspace root)
    2. Chiamare configure_workspace(agent_id, workspace_path) per scrivere
       .vscode/mcp.json automaticamente senza intervento manuale dell'utente
    3. Comunicare all'utente: "Ho scritto .vscode/mcp.json. Esegui
       'MCP: List Servers' dal Command Palette per attivare il server Looker."
    4. Attendere conferma prima di procedere con la sessione.
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
app = mcp.http_app()


@mcp.tool()
async def configure_workspace(agent_id: str, workspace_path: str, credentials: dict | None = None) -> str:
    """
    Scrive la configurazione MCP dell'agente nel file .vscode/mcp.json
    della cartella di lavoro corrente, evitando la configurazione manuale.

    Usare questo tool subito dopo get_agent quando mcp_servers non è vuoto.
    workspace_path è il path assoluto della cartella root del progetto corrente.

    WORKFLOW CREDENZIALI — seguire sempre questo ordine:
    1. Leggere env_required dalla risposta di get_agent
    2. Se env_required non è vuoto, chiedere all'utente i valori nel chat
       (es. "Per configurare Looker ho bisogno di LOOKER_CLIENT_ID e LOOKER_CLIENT_SECRET")
    3. Chiamare questo tool passando i valori raccolti come dizionario:
       credentials={"LOOKER_CLIENT_ID": "valore", "LOOKER_CLIENT_SECRET": "valore"}
    4. I valori vengono scritti in .vscode/mcp.json e .vscode/mcp.json viene
       aggiunto automaticamente al .gitignore del workspace
    5. Comunicare all'utente di eseguire 'MCP: List Servers' per attivare il server

    Se credentials è omesso, VS Code userà ${input:...} e chiederà i valori
    al primo avvio salvandoli nel keychain del SO.
    """
    return await _configure_workspace(provider, agent_id, workspace_path, credentials)


def run():
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        log_level="info",
    )


if __name__ == "__main__":
    run()
