from typing import Any, Protocol


class Provider(Protocol):
    """Интерфейс провайдера, публикующего команды бронирования и отмены."""

    @property
    def name(self) -> str:
        """Имя провайдера для маршрутизации входных payload-ов."""
        ...

    async def book(self, payload: dict[str, Any]) -> None:
        """Публикует команду на бронирование."""
        ...

    async def cancel(self, payload: dict[str, Any]) -> None:
        """Публикует команду на отмену бронирования."""
        ...
