from typing import Any

def _active_user_lowering_ops_default() -> OrderedSet[Any]:
    """Default factory for active_user_lowering_ops - returns persisted empty set."""
    rv: OrderedSet[Any] = OrderedSet()
    setattr(threadlocal, _active_user_lowering_ops._key, rv)
    return rv

