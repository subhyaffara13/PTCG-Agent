
def test_sympy__functions__elementary__complexes__principal_branch():
    from sympy.functions.elementary.complexes import principal_branch
    assert _test_args(principal_branch(x, y))

