
def test_unevaluated_CompoundDist():
    # these tests need to be removed once they work with evaluation as they are currently not
    # evaluated completely in sympy.
    R = Rayleigh('R', 4)
    X = Normal('X', 3, R)
    ans = '''
        Piecewise(((-sqrt(pi)*sinh(x/4 - 3/4) + sqrt(pi)*cosh(x/4 - 3/4))/(
        8*sqrt(pi)), Abs(arg(x - 3)) <= pi/4), (Integral(sqrt(2)*exp(-(x - 3)
        **2/(2*R**2))*exp(-R**2/32)/(32*sqrt(pi)), (R, 0, oo)), True))'''
    assert streq(density(X)(x), ans)

    expre = '''
        Integral(X*Integral(sqrt(2)*exp(-(X-3)**2/(2*R**2))*exp(-R**2/32)/(32*
        sqrt(pi)),(R,0,oo)),(X,-oo,oo))'''
    with ignore_warnings(UserWarning): ### TODO: Restore tests once warnings are removed
        assert streq(E(X, evaluate=False).rewrite(Integral), expre)

    X = Poisson('X', 1)
    Y = Poisson('Y', X)
    Z = Poisson('Z', Y)
    exprd = Sum(exp(-Y)*Y**x*Sum(exp(-1)*exp(-X)*X**Y/(factorial(X)*factorial(Y)
                ), (X, 0, oo))/factorial(x), (Y, 0, oo))
    assert density(Z)(x) == exprd

    N = Normal('N', 1, 2)
    M = Normal('M', 3, 4)
    D = Normal('D', M, N)
    exprd = '''
        Integral(sqrt(2)*exp(-(N-1)**2/8)*Integral(exp(-(x-M)**2/(2*N**2))*exp
        (-(M-3)**2/32)/(8*pi*N),(M,-oo,oo))/(4*sqrt(pi)),(N,-oo,oo))'''
    assert streq(density(D, evaluate=False)(x), exprd)

