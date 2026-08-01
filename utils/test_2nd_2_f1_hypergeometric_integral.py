
def test_2nd_2F1_hypergeometric_integral():
    eq = x*(x-1)*f(x).diff(x, 2) + (-1+ S(7)/2*x)*f(x).diff(x) + f(x)
    sol = Eq(f(x), (C1 + C2*Integral(exp(Integral((1 - x/2)/(x*(x - 1)), x))/(1 -
          x/2)**2, x))*exp(Integral(1/(x - 1), x)/4)*exp(-Integral(7/(x -
          1), x)/4)*hyper((S(1)/2, -1), (1,), x))
    assert sol == dsolve(eq, hint='2nd_hypergeometric_Integral')
    assert checkodesol(eq, sol) == (True, 0)

