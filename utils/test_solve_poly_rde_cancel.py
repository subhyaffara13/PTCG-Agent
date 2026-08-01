
def test_solve_poly_rde_cancel():
    # exp
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(t, t)]})
    assert cancel_exp(Poly(2*x, t), Poly(2*x, t), 0, DE) == \
        Poly(1, t)
    assert cancel_exp(Poly(2*x, t), Poly((1 + 2*x)*t, t), 1, DE) == \
        Poly(t, t)
    # TODO: Add more exp tests, including tests that require is_deriv_in_field()

    # primitive
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(1/x, t)]})

    # If the DecrementLevel context manager is working correctly, this shouldn't
    # cause any problems with the further tests.
    raises(NonElementaryIntegralException, lambda: cancel_primitive(Poly(1, t), Poly(t, t), oo, DE))

    assert cancel_primitive(Poly(1, t), Poly(t + 1/x, t), 2, DE) == \
        Poly(t, t)
    assert cancel_primitive(Poly(4*x, t), Poly(4*x*t**2 + 2*t/x, t), 3, DE) == \
        Poly(t**2, t)

