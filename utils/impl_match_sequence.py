from typing import Any

def impl_MATCH_SEQUENCE(a: object) -> TypeGuard[Sequence[Any]]:
    return isinstance(a, Sequence) and not isinstance(a, (str, bytes, bytearray))

