
def test_rewrite_MaxMin_as_Heaviside():
    from sympy.abc import x
    assert Max(0, x).rewrite(Heaviside) == x*Heaviside(x)
    assert Max(3, x).rewrite(Heaviside) == x*Heaviside(x - 3) + \
        3*Heaviside(-x + 3)
    assert Max(0, x+2, 2*x).rewrite(Heaviside) == \
        2*x*Heaviside(2*x)*Heaviside(x - 2) + \
        (x + 2)*Heaviside(-x + 2)*Heaviside(x + 2)

    assert Min(0, x).rewrite(Heaviside) == x*Heaviside(-x)
    assert Min(3, x).rewrite(Heaviside) == x*Heaviside(-x + 3) + \
        3*Heaviside(x - 3)
    assert Min(x, -x, -2).rewrite(Heaviside) == \
        x*Heaviside(-2*x)*Heaviside(-x - 2) - \
        x*Heaviside(2*x)*Heaviside(x - 2) \
        - 2*Heaviside(-x + 2)*Heaviside(x + 2)

