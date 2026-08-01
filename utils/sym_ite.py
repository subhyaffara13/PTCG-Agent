
def sym_ite(b, t, f):
    """SymInt-aware utility for ternary operator (``t if b else f``.)"""
    if overrides.has_torch_function((b, t, f)):
        return overrides.handle_torch_function(sym_ite, (b, t, f), b, t, f)
    if not isinstance(b, (SymBool, builtins.bool)):
        raise AssertionError(f"expected SymBool or bool, got {type(b)}")
    if type(t) is not type(f):
        raise AssertionError(f"type mismatch: {type(t)} vs {type(f)}")
    if isinstance(b, SymBool):
        return b.__sym_ite__(t, f)
    return t if b else f


def sym_ite(b: BOOL, t: TTensor, f: TTensor) -> TTensor:
    """sym_ite(SymBool b, Tensor t, Tensor f) -> Tensor"""
    return op.Where(b, t, f)

