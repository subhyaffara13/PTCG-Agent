from typing import Any, Callable

def _transform_diagnose_call_message_formatter(
    run: Callable,
    self: Transform,
    *args: Any,
    **kwargs: Any,
) -> str:
    return f"Running {self.__class__.__name__} pass. "

