
def test_sympy__stats__frv__FiniteDomain():
    from sympy.stats.frv import FiniteDomain
    assert _test_args(FiniteDomain({(x, 1), (x, 2)}))  # x can be 1 or 2

