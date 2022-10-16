import asyncio
from typing import Any, Callable, Coroutine, Optional

from .enums import Opcode

Listener = Callable[..., Coroutine[Any, Any, None]]


class Dispatcher:
    def __init__(self, *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        self.loop = loop or asyncio.get_event_loop()
        self._listeners: dict[Opcode, list[Listener]] = {}
        self._tasks: list[asyncio.Task[Any]] = []
        self._ready = asyncio.Event()
        self._closed = False

    def listen(self, event: Opcode) -> Callable[[Listener], Listener]:
        """A decorator that adds a listener to the dispatcher.

        Parameters
        ----------
        event : Opcode
            The event to listen for.

        Returns
        -------
        Callable[[Listener], Listener]
            The decorator.
        """

        def decorator(callback: Listener) -> Listener:
            self.add_listener(event, callback)
            return callback

        return decorator

    def add_listener(self, event: Opcode, callback: Listener) -> None:
        """Add a listener to the dispatcher.

        Parameters
        ----------
        event : Opcode
            The event to listen for.
        callback : Listener
            The callback to call when the event is dispatched.
        """
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)

    def remove_listener(self, event: Opcode, callback: Listener) -> None:
        """Remove a listener from the dispatcher.

        Parameters
        ----------
        event : Opcode
            The event to remove the listener from.
        callback : Listener
            The listener to remove.
        """
        if event not in self._listeners:
            return
        self._listeners[event].remove(callback)

    def remove_all_listeners(self, event: Opcode) -> None:
        """Remove all listeners from the dispatcher.

        Parameters
        ----------
        event : Opcode
            The event to remove all listeners from.
        """
        if event not in self._listeners:
            return
        del self._listeners[event]

    async def dispatch(self, event: Opcode, *args: Any, **kwargs: Any) -> None:
        """Dispatch an event to all listeners.

        Parameters
        ----------
        event : Opcode
            The event to dispatch.
        """
        if event not in self._listeners:
            return
        for listener in self._listeners[event]:
            # FIXME
            await listener(*args, **kwargs)

    async def wait_until_ready(self) -> None:
        """Wait until the dispatcher is ready."""
        await self._ready.wait()

    def close(self) -> None:
        """Close the dispatcher."""
        self._closed = True
        for task in self._tasks:
            task.cancel()
