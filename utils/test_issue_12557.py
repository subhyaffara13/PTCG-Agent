
def test_issue_12557():
    '''
    # 3200 seconds to compute the fourier part of issue
    import sympy as sym
    x,y,z,t = sym.symbols('x y z t')
    k = sym.symbols("k", integer=True)
    fourier = sym.fourier_series(sym.cos(k*x)*sym.sqrt(x**2),
                                 (x, -sym.pi, sym.pi))
    assert fourier == FourierSeries(
    sqrt(x**2)*cos(k*x), (x, -pi, pi), (Piecewise((pi**2,
    Eq(k, 0)), (2*(-1)**k/k**2 - 2/k**2, True))/(2*pi),
    SeqFormula(Piecewise((pi**2, (Eq(_n, 0) & Eq(k, 0)) | (Eq(_n, 0) &
    Eq(_n, k) & Eq(k, 0)) | (Eq(_n, 0) & Eq(k, 0) & Eq(_n, -k)) | (Eq(_n,
    0) & Eq(_n, k) & Eq(k, 0) & Eq(_n, -k))), (pi**2/2, Eq(_n, k) | Eq(_n,
    -k) | (Eq(_n, 0) & Eq(_n, k)) | (Eq(_n, k) & Eq(k, 0)) | (Eq(_n, 0) &
    Eq(_n, -k)) | (Eq(_n, k) & Eq(_n, -k)) | (Eq(k, 0) & Eq(_n, -k)) |
    (Eq(_n, 0) & Eq(_n, k) & Eq(_n, -k)) | (Eq(_n, k) & Eq(k, 0) & Eq(_n,
    -k))), ((-1)**k*pi**2*_n**3*sin(pi*_n)/(pi*_n**4 - 2*pi*_n**2*k**2 +
    pi*k**4) - (-1)**k*pi**2*_n**3*sin(pi*_n)/(-pi*_n**4 + 2*pi*_n**2*k**2
    - pi*k**4) + (-1)**k*pi*_n**2*cos(pi*_n)/(pi*_n**4 - 2*pi*_n**2*k**2 +
    pi*k**4) - (-1)**k*pi*_n**2*cos(pi*_n)/(-pi*_n**4 + 2*pi*_n**2*k**2 -
    pi*k**4) - (-1)**k*pi**2*_n*k**2*sin(pi*_n)/(pi*_n**4 -
    2*pi*_n**2*k**2 + pi*k**4) +
    (-1)**k*pi**2*_n*k**2*sin(pi*_n)/(-pi*_n**4 + 2*pi*_n**2*k**2 -
    pi*k**4) + (-1)**k*pi*k**2*cos(pi*_n)/(pi*_n**4 - 2*pi*_n**2*k**2 +
    pi*k**4) - (-1)**k*pi*k**2*cos(pi*_n)/(-pi*_n**4 + 2*pi*_n**2*k**2 -
    pi*k**4) - (2*_n**2 + 2*k**2)/(_n**4 - 2*_n**2*k**2 + k**4),
    True))*cos(_n*x)/pi, (_n, 1, oo)), SeqFormula(0, (_k, 1, oo))))
    '''
    x = symbols("x", real=True)
    k = symbols('k', integer=True, finite=True)
    abs2 = lambda x: Piecewise((-x, x <= 0), (x, x > 0))
    assert integrate(abs2(x), (x, -pi, pi)) == pi**2
    func = cos(k*x)*sqrt(x**2)
    assert integrate(func, (x, -pi, pi)) == Piecewise(
        (2*(-1)**k/k**2 - 2/k**2, Ne(k, 0)), (pi**2, True))

