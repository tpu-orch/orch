from typing import Any, Protocol

from pydantic import BaseModel


class Provider(Protocol):
    name: str

    async def book(self, payload: dict[str, Any]) -> None: ...


class Payload(BaseModel):
    name: str
    payload: dict[str, Any]


class Orchestrator:
    def __init__(self, providers: list[Provider]) -> None:
        self.providers: dict[str, Provider] = {}
        for provider in providers:
            if provider.name in self.providers:
                raise ValueError(f"Duplicate provider name: {provider.name}")
            self.providers[provider.name] = provider

    async def run(self, payloads: list[Payload]) -> None:
        for item in payloads:
            if item.name not in self.providers:
                raise ValueError(f"Unknown provider: {item.name}")
            await self.providers[item.name].book(item.payload)
