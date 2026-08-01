
def test_integrate_nonlinear_no_specials():
    a, d, = Poly(x**2*t**5 + x*t**4 - nu**2*t**3 - x*(x**2 + 1)*t**2 - (x**2 -
    nu**2)*t - x**5/4, t), Poly(x**2*t**4 + x**2*(x**2 + 2)*t**2 + x**2 + x**4 + x**6/4, t)
    # f(x) == phi_nu(x), the logarithmic derivative of J_v, the Bessel function,
    # which has no specials (see Chapter 5, note 4 of Bronstein's book).
    f = Function('phi_nu')
    DE = DifferentialExtension(extension={'D': [Poly(1, x),
        Poly(-t**2 - t/x - (1 - nu**2/x**2), t)], 'Tfuncs': [f]})
    assert integrate_nonlinear_no_specials(a, d, DE) == \
        (-log(1 + f(x)**2 + x**2/2)/2 + (- 4 - x**2)/(4 + 2*x**2 + 4*f(x)**2), True)
    assert integrate_nonlinear_no_specials(Poly(t, t), Poly(1, t), DE) == \
        (0, False)

