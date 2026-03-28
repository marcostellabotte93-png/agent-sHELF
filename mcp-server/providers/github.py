import base64
import httpx
from .base import GitProvider


class GitHubProvider(GitProvider):
    def __init__(self, token: str, owner: str, repo: str, branch: str = "main"):
        self.base = f"https://api.github.com/repos/{owner}/{repo}/contents"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        self.branch = branch

    async def get_file(self, path: str) -> str:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(
                f"{self.base}/{path}",
                params={"ref": self.branch},
                headers=self.headers,
            )
            r.raise_for_status()
            data = r.json()
            return base64.b64decode(data["content"]).decode("utf-8")

    async def list_directory(self, path: str) -> list[str]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(
                f"{self.base}/{path}",
                params={"ref": self.branch},
                headers=self.headers,
            )
            r.raise_for_status()
            return [item["name"] for item in r.json() if item["type"] == "dir"]
