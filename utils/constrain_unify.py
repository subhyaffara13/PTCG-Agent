
def constrain_unify(a: torch.SymInt, b: torch.SymInt) -> None:
    """
    Given two SymInts, constrain them so that they must be equal.  NB:
    this will not work with SymInts that represent nontrivial expressions
    (yet!)
    """
    if not isinstance(a, SymInt):
        if not isinstance(b, SymInt):
            if a != b:
                raise AssertionError(f"Expected {a} == {b}")
            return
        else:
            shape_env = b.node.shape_env
    else:
        shape_env = a.node.shape_env

    shape_env._constrain_unify(a, b)

