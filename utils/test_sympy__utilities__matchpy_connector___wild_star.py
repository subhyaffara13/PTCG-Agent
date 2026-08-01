
def test_sympy__utilities__matchpy_connector__WildStar():
    from sympy.utilities.matchpy_connector import WildStar
    assert _test_args(WildStar("w___"))

