
def sym_eq(x: _T, y: _T) -> BoolLikeType:
    """
    Like ==, but when run on list/tuple, it will recursively test equality
    and use sym_and to join the results together, without guarding.
    """
    if isinstance(x, (tuple, list)) and isinstance(y, (list, tuple)):
        if len(x) != len(y):
            return False
        return functools.reduce(operator.and_, map(sym_eq, x, y), True)
    elif isinstance(x, (int, torch.SymInt)) and isinstance(y, (int, torch.SymInt)):
        return x == y
    else:
        raise AssertionError(f"unexpected sym_eq between {type(x)} {type(y)}")

