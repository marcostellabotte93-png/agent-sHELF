import json
from providers.base import GitProvider

SKILL_SIZE_THRESHOLD_BYTES = 10_000  # 10KB: sotto questa soglia carica tutto staticamente


def _build_vscode_mcp_config(mcp_servers: list) -> dict:
    """
    Genera il blocco .vscode/mcp.json pronto all'uso per i server MCP dell'agente.

    - Server HTTP (type: http): configurati con URL e header di autenticazione tramite
      VS Code input variables (password=True → salvate nel keychain del SO).
    - Server stdio (type: stdio o assente): configurati con command/args/env;
      devono essere aggiunti manualmente a ~/.vscode/mcp.json.
    """
    servers: dict = {}
    inputs: list = []

    for server in mcp_servers:
        name = server["name"]
        server_type = server.get("type", "stdio")

        if server_type == "http":
            cfg: dict = {"type": "http", "url": server["url"]}
            auth = server.get("auth", {})
            if auth.get("type") == "bearer":
                env_key = auth["env"]
                input_id = env_key.lower().replace("_", "-")
                header_name = auth.get("header", "Authorization")
                cfg["headers"] = {header_name: f"Bearer ${{input:{input_id}}}"}
                inputs.append({
                    "id": input_id,
                    "type": "promptString",
                    "description": env_key,
                    "password": True,
                })
            servers[name] = cfg
        else:
            # Server stdio: genera il blocco ma segnala che va in ~/.vscode/mcp.json
            cfg = {
                "command": server.get("command", ""),
                "args": server.get("args", []),
                "_note": "Aggiungere a ~/.vscode/mcp.json (non a .vscode/mcp.json)",
            }
            env_block: dict = {}
            for env_key in server.get("env_required", []):
                input_id = env_key.lower().replace("_", "-")
                env_block[env_key] = f"${{input:{input_id}}}"
                inputs.append({
                    "id": input_id,
                    "type": "promptString",
                    "description": env_key,
                    "password": True,
                })
            for env_key, default in server.get("env_optional", {}).items():
                env_block[env_key] = default
            if env_block:
                cfg["env"] = env_block
            servers[name] = cfg

    result: dict = {"servers": servers}
    if inputs:
        result["inputs"] = inputs
    return result


async def get_agent(provider: GitProvider, id: str) -> str:
    """
    Scarica e restituisce un agente completo dalla libreria.

    Restituisce un oggetto JSON con:
    - system_prompt: contenuto delle skills core concatenate (da iniettare nel contesto)
    - available_skills: lista delle skills extended disponibili on-demand
    - mcp_servers: configurazione dei server MCP esterni da avviare (se presenti)
    - metadata: id, name, version, category

    Il chiamante deve usare system_prompt come system prompt della sessione.

    Se mcp_servers non è vuoto, seguire questo processo:
    1. Mostrare all'utente la configurazione del server (name, command, args)
    2. Chiedere i valori delle variabili in env_required (non mostrarle nei log)
    3. Istruire l'utente ad aggiungere il blocco server nel proprio ~/.vscode/mcp.json:
       {
         "servers": {
           "<name>": {
             "command": "<command>",
             "args": [...],
             "env": { "<VAR>": "<valore fornito dall'utente>" }
           }
         }
       }
    4. Chiedere all'utente di riavviare VS Code / ricaricare i server MCP
    5. Confermare che il server è attivo prima di procedere con la sessione
    I valori in env_optional hanno un default e non bloccano l'avvio.
    """
    raw_manifest = await provider.get_file(f"agents/{id}/agent.json")
    manifest = json.loads(raw_manifest)

    # Carica le skills core
    core_parts = []
    total_bytes = 0
    for skill_path in manifest["skills"]["core"]:
        content = await provider.get_file(f"agents/{id}/{skill_path}")
        core_parts.append(content)
        total_bytes += len(content.encode())

    # Valuta se caricare anche le extended staticamente
    extended_paths = manifest["skills"].get("extended", [])
    extended_static = []

    if total_bytes < SKILL_SIZE_THRESHOLD_BYTES and extended_paths:
        for skill_path in extended_paths:
            content = await provider.get_file(f"agents/{id}/{skill_path}")
            extended_static.append(content)
            total_bytes += len(content.encode())

    system_prompt_parts = core_parts + extended_static
    system_prompt = "\n\n---\n\n".join(system_prompt_parts)

    # Se le extended sono state caricate staticamente, non esporle come tool
    available_skills = [] if extended_static else [
        {"name": p.replace("skills/", "").replace(".md", ""), "path": p}
        for p in extended_paths
    ]

    raw_mcp_servers = manifest.get("mcp_servers", [])
    vscode_mcp_config = _build_vscode_mcp_config(raw_mcp_servers) if raw_mcp_servers else None

    return json.dumps({
        "id": manifest["id"],
        "name": manifest["name"],
        "version": manifest["version"],
        "category": manifest.get("category", ""),
        "system_prompt": system_prompt,
        "available_skills": available_skills,
        "mcp_servers": raw_mcp_servers,
        "vscode_mcp_config": vscode_mcp_config,
    }, ensure_ascii=False, indent=2)
