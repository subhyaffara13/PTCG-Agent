
def test_integrate_with_complex_constants():
    K = Symbol('K', positive=True)
    x = Symbol('x', real=True)
    m = Symbol('m', real=True)
    t = Symbol('t', real=True)
    assert integrate(exp(-I*K*x**2+m*x), x) == sqrt(pi)*exp(-I*m**2
                    /(4*K))*erfi((-2*I*K*x + m)/(2*sqrt(K)*sqrt(-I)))/(2*sqrt(K)*sqrt(-I))
    assert integrate(1/(1 + I*x**2), x) == (-I*(sqrt(-I)*log(x - I*sqrt(-I))/2
            - sqrt(-I)*log(x + I*sqrt(-I))/2))
    assert integrate(exp(-I*x**2), x) == sqrt(pi)*erf(sqrt(I)*x)/(2*sqrt(I))

    assert integrate((1/(exp(I*t)-2)), t) == -t/2 - I*log(exp(I*t) - 2)/2
    assert integrate((1/(exp(I*t)-2)), (t, 0, 2*pi)) == -pi

