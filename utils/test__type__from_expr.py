
def test_Type__from_expr():
    assert Type.from_expr(i) == integer
    u = symbols('u', real=True)
    assert Type.from_expr(u) == real
    assert Type.from_expr(n) == integer
    assert Type.from_expr(3) == integer
    assert Type.from_expr(3.0) == real
    assert Type.from_expr(3+1j) == complex_
    raises(ValueError, lambda: Type.from_expr(sum))

