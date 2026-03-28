import os
from .base import GitProvider
from .github import GitHubProvider


def create_provider() -> GitProvider:
    provider_type = os.environ.get("GIT_PROVIDER", "github")

    match provider_type:
        case "github":
            return GitHubProvider(
                token=_require("GITHUB_TOKEN"),
                owner=_require("GITHUB_OWNER"),
                repo=_require("GITHUB_REPO"),
                branch=os.getenv("GITHUB_BRANCH", "main"),
            )
        case _:
            raise ValueError(
                f"GIT_PROVIDER non supportato: '{provider_type}'. "
                "Valore valido: github"
            )


def _require(key: str) -> str:
    val = os.getenv(key)
    if not val:
        raise EnvironmentError(f"Variabile d'ambiente obbligatoria mancante: {key}")
    return val
