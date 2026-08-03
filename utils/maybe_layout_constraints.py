from typing import Any, Callable

def maybe_layout_constraints(fn: Callable[..., Any]) -> Callable[..., Any] | None:
    """Get layout constraints. Returns None if there are no layout constraints."""
    if not isinstance(fn, torch._ops.OpOverload):
        # Only OpOverloads have layout constraints.
        return None

    if maybe_layout_tag := get_layout_constraint_tag(fn, with_default=False):
        return tag_to_layout_constraint(maybe_layout_tag)

    if fn in _maybe_layout_constraints:
        return _maybe_layout_constraints[fn]
    return None

