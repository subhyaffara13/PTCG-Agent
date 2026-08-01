
def test_collect_pr19431():
    """Unevaluated collect with respect to a product"""
    a = symbols('a')
    assert collect(a**2*(a**2 + 1), a**2, evaluate=False)[a**2] == (a**2 + 1)

