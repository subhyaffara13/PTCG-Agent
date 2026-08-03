from typing import Callable

def has_side_effect(fn: Callable[_P, _R]) -> Callable[_P, _R]:
    """
    Registers a function to not be dead code eliminated by
    fx.graph.eliminate_dead_code

    NOTE: For new operators, please do not add to this set!
    Instead, consider using the effects system via
    torch.library._register_effectful_op() for operators.

    This _side_effectful_functions set is only for:
    - Legacy functions that aren't operators (e.g., profiler ops, asserts)
    - Things that cannot be marked via the normal effects system
    """
    _side_effectful_functions.add(fn)
    return fn

