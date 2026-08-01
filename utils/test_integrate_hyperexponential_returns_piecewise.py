
def test_integrate_hyperexponential_returns_piecewise():
    a, b = symbols('a b')
    DE = DifferentialExtension(a**x, x)
    assert integrate_hyperexponential(DE.fa, DE.fd, DE) == (Piecewise(
        (exp(x*log(a))/log(a), Ne(log(a), 0)), (x, True)), 0, True)
    DE = DifferentialExtension(a**(b*x), x)
    assert integrate_hyperexponential(DE.fa, DE.fd, DE) == (Piecewise(
        (exp(b*x*log(a))/(b*log(a)), Ne(b*log(a), 0)), (x, True)), 0, True)
    DE = DifferentialExtension(exp(a*x), x)
    assert integrate_hyperexponential(DE.fa, DE.fd, DE) == (Piecewise(
        (exp(a*x)/a, Ne(a, 0)), (x, True)), 0, True)
    DE = DifferentialExtension(x*exp(a*x), x)
    assert integrate_hyperexponential(DE.fa, DE.fd, DE) == (Piecewise(
        ((a*x - 1)*exp(a*x)/a**2, Ne(a**2, 0)), (x**2/2, True)), 0, True)
    DE = DifferentialExtension(x**2*exp(a*x), x)
    assert integrate_hyperexponential(DE.fa, DE.fd, DE) == (Piecewise(
        ((x**2*a**2 - 2*a*x + 2)*exp(a*x)/a**3, Ne(a**3, 0)),
        (x**3/3, True)), 0, True)
    DE = DifferentialExtension(x**y + z, y)
    assert integrate_hyperexponential(DE.fa, DE.fd, DE) == (Piecewise(
        (exp(log(x)*y)/log(x), Ne(log(x), 0)), (y, True)), z, True)
    DE = DifferentialExtension(x**y + z + x**(2*y), y)
    assert integrate_hyperexponential(DE.fa, DE.fd, DE) == (Piecewise(
        ((exp(2*log(x)*y)*log(x) +
            2*exp(log(x)*y)*log(x))/(2*log(x)**2), Ne(2*log(x)**2, 0)),
            (2*y, True),
        ), z, True)

