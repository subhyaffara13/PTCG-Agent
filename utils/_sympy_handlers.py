
def _sympy_handlers() -> dict[type[sympy.Expr], Callable[..., Any]]:
    """
    Returns a dict mapping sympy types to Python callables
    (e.g. ``sympy.Mul`` -> ``operator.mul``, ``sympy.Add`` -> ``torch.sym_sum``).
    """
    import sympy

    import torch.utils._sympy.interp

    handlers = {}
    for k, v in torch.utils._sympy.interp.handlers().items():
        op = getattr(operator, v, None)
        if op is not None:
            handlers[k] = op

    # sympy.Add is n-ary (e.g. Add(a, b, c)) but operator.add is binary.
    # torch.sym_sum handles n-ary integer addition and accepts both
    # sym_sum([a, b, c]) and sym_sum(a, b, c).
    handlers[sympy.Add] = torch.sym_sum
    return handlers

