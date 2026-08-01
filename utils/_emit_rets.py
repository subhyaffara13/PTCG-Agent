
def _emit_rets(returns):
    if len(returns) == 1:
        return _emit_ret(returns[0])
    return f"Tuple[{', '.join(_emit_ret(r) for r in returns)}]"

