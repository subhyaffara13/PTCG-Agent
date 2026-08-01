
def maybe_free_symbols(s: object) -> OrderedSet[Symbol]:
    if isinstance(s, (SymTypes, Expr)):
        # This branch should be impossible in return position
        return free_symbols(s)
    elif isinstance(s, (tuple, list)):
        r = OrderedSet[sympy.Symbol]()
        for t in s:
            r |= maybe_free_symbols(t)
        return r
    elif isinstance(s, torch.Tensor):
        # This branch is impossible in constant-args position
        return free_symbols(s)
    else:
        return OrderedSet()

