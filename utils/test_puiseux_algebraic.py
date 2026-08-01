
def test_puiseux_algebraic(): # https://github.com/sympy/sympy/issues/24395

    K = QQ.algebraic_field(sqrt(2))
    sqrt2 = K.from_sympy(sqrt(2))
    x, y = symbols('x, y')
    R, xr, yr = puiseux_ring([x, y], K)
    p = (1+sqrt2)*xr**QQ(1,2) + (1-sqrt2)*yr**QQ(2,3)

    assert p.to_dict() == {(QQ(1,2),QQ(0)):1+sqrt2, (QQ(0),QQ(2,3)):1-sqrt2}
    assert p.as_expr() == (1 + sqrt(2))*x**(S(1)/2) + (1 - sqrt(2))*y**(S(2)/3)

