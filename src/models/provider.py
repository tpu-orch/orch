from typing import Protocol, Any


class Provider(Protocol):
    name: str

    async def book(self, payload: dict[str, Any]) -> None: ...
    async def cancel(self, payload: dict[str, Any]) -> None: ...
