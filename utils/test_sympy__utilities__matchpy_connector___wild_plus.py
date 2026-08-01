
def test_sympy__utilities__matchpy_connector__WildPlus():
    from sympy.utilities.matchpy_connector import WildPlus
    assert _test_args(WildPlus("w__"))

