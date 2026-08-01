
def test_sympy__assumptions__wrapper__AssumptionsWrapper():
    from sympy.assumptions.wrapper import AssumptionsWrapper
    assert _test_args(AssumptionsWrapper(x, Q.positive(x)))

