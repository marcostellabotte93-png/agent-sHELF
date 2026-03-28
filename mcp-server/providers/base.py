from abc import ABC, abstractmethod


class GitProvider(ABC):
    @abstractmethod
    async def get_file(self, path: str) -> str:
        """Restituisce il contenuto di un file come stringa UTF-8."""

    @abstractmethod
    async def list_directory(self, path: str) -> list[str]:
        """Restituisce i nomi delle sottocartelle dirette in path."""
