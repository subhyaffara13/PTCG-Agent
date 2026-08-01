
def test_issue_17354():
    from sympy.core.symbol import (Wild, symbols)
    x, y = symbols("x y", real=True)
    a, b = symbols("a b", cls=Wild)
    assert ((0 <= x).reversed | (y <= x)).match((1/a <= b) | (a <= b)) is None

