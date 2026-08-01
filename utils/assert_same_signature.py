
def assert_same_signature(func1, func2):
    """
    Assert that `func1` and `func2` have the same arguments,
    i.e. same parameter count, names and kinds.

    :param func1: First function to check
    :param func2: Second function to check
    """
    params1 = inspect.signature(func1).parameters
    params2 = inspect.signature(func2).parameters

    assert len(params1) == len(params2)
    assert all([
        params1[p].name == params2[p].name and
        params1[p].kind == params2[p].kind
        for p in params1
    ])

