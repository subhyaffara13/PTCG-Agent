
def test_rcode_Piecewise_deep():
    p = rcode(2*Piecewise((x, x < 1), (x + 1, x < 2), (x**2, True)))
    assert p == "2*ifelse(x < 1,x,ifelse(x < 2,x + 1,x^2))"
    expr = x*y*z + x**2 + y**2 + Piecewise((0, x < 0.5), (1, True)) + cos(z) - 1
    p = rcode(expr)
    ref="x^2 + x*y*z + y^2 + ifelse(x < 0.5,0,1) + cos(z) - 1"
    assert p == ref

    ref="c = x^2 + x*y*z + y^2 + ifelse(x < 0.5,0,1) + cos(z) - 1;"
    p = rcode(expr, assign_to='c')
    assert p == ref

