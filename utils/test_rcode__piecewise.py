
def test_rcode_Piecewise():
    expr = Piecewise((x, x < 1), (x**2, True))
    res=rcode(expr)
    ref="ifelse(x < 1,x,x^2)"
    assert res == ref
    tau=Symbol("tau")
    res=rcode(expr,tau)
    ref="tau = ifelse(x < 1,x,x^2);"
    assert res == ref

    expr = 2*Piecewise((x, x < 1), (x**2, x<2), (x**3,True))
    assert rcode(expr) == "2*ifelse(x < 1,x,ifelse(x < 2,x^2,x^3))"
    res = rcode(expr, assign_to='c')
    assert res == "c = 2*ifelse(x < 1,x,ifelse(x < 2,x^2,x^3));"

    # Check that Piecewise without a True (default) condition error
    #expr = Piecewise((x, x < 1), (x**2, x > 1), (sin(x), x > 0))
    #raises(ValueError, lambda: rcode(expr))
    expr = 2*Piecewise((x, x < 1), (x**2, x<2))
    assert(rcode(expr))== "2*ifelse(x < 1,x,ifelse(x < 2,x^2,NA))"

