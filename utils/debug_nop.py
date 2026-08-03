from typing import Any, Callable

def debug_nop(
    fx_g: fx.GraphModule, _: Any
) -> Callable[[DebugInterpreter, Any, dict[Node, Any] | None, bool], Any]:
    """
    Returns a (slow) interpreter over the FX graph module that also checks
    various debugging properties (e.g., that tracing strides matched real
    strides.)
    """
    return DebugInterpreter(fx_g).run

