from typing import Any

def nop(fx_g: fx.GraphModule, _: Any) -> fx.GraphModule:
    """
    Returns the :attr:`fx_g` Fx graph module as it is. This is a no-op compiler
    and can be used to check accuracy.

    .. warning::
        This API is experimental and likely to change.

    """
    return fx_g


def nop(x):
    return x  # AOT autograd handles this for us

