
def resolve_shape_to_proxy(
    shape: list[int | torch.SymInt], bound_symbols: dict[Any, Any]
):
    """
    Given a list of symints/ints, this function returns a calculated expression of bound_symbols' values.
    When we trace this function, we'll get a graph with call_function nodes that describes how the shape expr is
    computed from bound_symbols' values.

    Suppose shape = (s1*s2, s1+s2) and bound_symbols = {s1: arg0, s2: arg1}, the result will be
    (arg0 * arg1, arg0 + arg1).
    """
    from torch.utils._sympy.interp import sympy_interp
    from torch.utils._sympy.reference import PythonReferenceAnalysis

    ret = []
    for s in shape:
        if isinstance(s, torch.SymInt):
            ret.append(
                sympy_interp(
                    PythonReferenceAnalysis,
                    bound_symbols,
                    s.node.expr,
                ),
            )
        else:
            assert isinstance(s, int)
            ret.append(s)
    return ret

