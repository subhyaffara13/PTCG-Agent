
def sym_constrain_range(size, min=None, max=None):
    # Avoid importing sympy at a module level
    from torch.fx.experimental.symbolic_shapes import constrain_range

    if isinstance(size, (SymFloat, SymBool)):
        raise ValueError("Constraining SymFloat or Symbool is nyi")
    constrain_range(size, min=min, max=max)


def sym_constrain_range(a, min=None, max=None):
    return None

