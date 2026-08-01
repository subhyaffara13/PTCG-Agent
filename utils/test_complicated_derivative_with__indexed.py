
def test_complicated_derivative_with_Indexed():
    x, y = symbols("x,y", cls=IndexedBase)
    sigma = symbols("sigma")
    i, j, k = symbols("i,j,k")
    m0,m1,m2,m3,m4,m5 = symbols("m0:6")
    f = Function("f")

    expr = f((x[i] - y[i])**2/sigma)
    _xi_1 = symbols("xi_1", cls=Dummy)
    assert expr.diff(x[m0]).dummy_eq(
        (x[i] - y[i])*KroneckerDelta(i, m0)*\
        2*Subs(
            Derivative(f(_xi_1), _xi_1),
            (_xi_1,),
            ((x[i] - y[i])**2/sigma,)
        )/sigma
    )
    assert expr.diff(x[m0]).diff(x[m1]).dummy_eq(
        2*KroneckerDelta(i, m0)*\
        KroneckerDelta(i, m1)*Subs(
            Derivative(f(_xi_1), _xi_1),
            (_xi_1,),
            ((x[i] - y[i])**2/sigma,)
         )/sigma + \
        4*(x[i] - y[i])**2*KroneckerDelta(i, m0)*KroneckerDelta(i, m1)*\
        Subs(
            Derivative(f(_xi_1), _xi_1, _xi_1),
            (_xi_1,),
            ((x[i] - y[i])**2/sigma,)
        )/sigma**2
    )

