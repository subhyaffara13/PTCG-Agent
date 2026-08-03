from typing import Any

def _delegate(op: str) -> Any:
    def delegate(
        self: IFDRational, *args: tuple[float, ...]
    ) -> bool | float | Fraction:
        return getattr(self._val, op)(*args)

    return delegate

