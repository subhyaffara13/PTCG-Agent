
def same_shape(a: ShapeType, b: ShapeType, *, allow_rhs_unbacked=False) -> bool:
    from torch.fx.experimental.symbolic_shapes import guard_or_true

    if len(a) != len(b):
        return False

    for x, y in zip(a, b):
        if allow_rhs_unbacked:
            if isinstance(y, torch.SymInt):
                continue

        # if we do not know, then they are not the same.
        if guard_or_true(x != y):
            return False

    return True

