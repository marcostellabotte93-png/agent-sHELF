import json
from providers.base import GitProvider


async def get_skill(provider: GitProvider, agent_id: str, skill_name: str) -> str:
    """
    Carica una skill extended on-demand per un agente attivo.

    Usare questo tool quando durante la sessione emerge la necessità
    di una competenza specifica non inclusa nel system prompt iniziale.

    skill_name è il nome del file senza path e senza .md
    (es. 'python-review' per 'skills/python-review.md').
    """
    raw_manifest = await provider.get_file(f"agents/{agent_id}/agent.json")
    manifest = json.loads(raw_manifest)

    extended_paths = manifest["skills"].get("extended", [])
    match = next(
        (p for p in extended_paths if skill_name in p),
        None,
    )

    if not match:
        available = [p.replace("skills/", "").replace(".md", "") for p in extended_paths]
        raise ValueError(
            f"Skill '{skill_name}' non trovata per l'agente '{agent_id}'. "
            f"Skills disponibili: {available}"
        )

    content = await provider.get_file(f"agents/{agent_id}/{match}")
    return json.dumps({
        "agent_id": agent_id,
        "skill_name": skill_name,
        "content": content,
    }, ensure_ascii=False, indent=2)
