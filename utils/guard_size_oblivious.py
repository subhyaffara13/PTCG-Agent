
def guard_size_oblivious(expr: torch.SymBool | bool) -> bool:
    """
    Perform a guard on a symbolic boolean expression in a size oblivious way.
    This is typically used when a non-oblivious test would result in a guard
    on a data dependent value of which we don't know the value of at compile time.
    When a guard is tested this way, we may diverge in behavior from how regular
    PyTorch semantics would treat it.  For more information, see
    https://github.com/pytorch/pytorch/pull/118579
    """
    if isinstance(expr, torch.SymBool):
        return expr.node.guard_size_oblivious("", 0)
    else:
        if not isinstance(expr, bool):
            raise AssertionError(f"Expected bool, got {type(expr)}")
        return expr

