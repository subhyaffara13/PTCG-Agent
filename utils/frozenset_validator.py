from typing import Any

def frozenset_validator(v: Any) -> FrozenSet[Any]:
    if isinstance(v, frozenset):
        return v
    elif sequence_like(v):
        return frozenset(v)
    else:
        raise errors.FrozenSetError()

