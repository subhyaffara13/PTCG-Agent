from typing import Callable

def func_to_graphable(
    func: Callable[..., object],
) -> tuple[list[object], pytree.TreeSpec]:
    """
    Pack and flatten a function type into graphable types.
    This is useful for legalizing the function argument of `flat_apply`.
    """
    return pytree.tree_flatten(_ConstantFunction(func))

