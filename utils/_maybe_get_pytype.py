
def _maybe_get_pytype(t):
    if t is torch.SymFloat:
        return float
    elif t is torch.SymInt:
        return int
    elif t is torch.SymBool:
        return bool
    else:
        return t

