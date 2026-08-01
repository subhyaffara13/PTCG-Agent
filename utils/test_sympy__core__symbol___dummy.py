
def test_sympy__core__symbol__Dummy():
    from sympy.core.symbol import Dummy
    assert _test_args(Dummy('t'))

