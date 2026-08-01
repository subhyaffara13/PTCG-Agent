
def test_is_algebraic_expr():
    assert sqrt(3).is_algebraic_expr(x) is True
    assert sqrt(3).is_algebraic_expr() is True

    eq = ((1 + x**2)/(1 - y**2))**(S.One/3)
    assert eq.is_algebraic_expr(x) is True
    assert eq.is_algebraic_expr(y) is True

    assert (sqrt(x) + y**(S(2)/3)).is_algebraic_expr(x) is True
    assert (sqrt(x) + y**(S(2)/3)).is_algebraic_expr(y) is True
    assert (sqrt(x) + y**(S(2)/3)).is_algebraic_expr() is True

    assert (cos(y)/sqrt(x)).is_algebraic_expr() is False
    assert (cos(y)/sqrt(x)).is_algebraic_expr(x) is True
    assert (cos(y)/sqrt(x)).is_algebraic_expr(y) is False
    assert (cos(y)/sqrt(x)).is_algebraic_expr(x, y) is False

