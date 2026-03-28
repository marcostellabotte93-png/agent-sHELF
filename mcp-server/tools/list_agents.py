import json
from providers.base import GitProvider


async def list_agents(provider: GitProvider) -> str:
    """
    Lista tutti gli agenti disponibili nella libreria agent-shelf.
    Restituisce un array JSON con metadati (id, name, version, category, description, author).
    Non include il contenuto dei system prompt o delle skills.
    """
    agent_dirs = await provider.list_directory("agents")
    manifests = []
    for agent_dir in agent_dirs:
        try:
            raw = await provider.get_file(f"agents/{agent_dir}/agent.json")
            manifest = json.loads(raw)
            manifests.append({
                k: manifest[k]
                for k in ["id", "name", "version", "category", "description", "author"]
                if k in manifest
            })
        except Exception as e:
            manifests.append({"id": agent_dir, "error": str(e)})
    return json.dumps(manifests, ensure_ascii=False, indent=2)
