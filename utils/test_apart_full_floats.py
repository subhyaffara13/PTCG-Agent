
def test_apart_full_floats():
    # https://github.com/sympy/sympy/issues/26648
    f = (
        6.43369157032015e-9*x**3 + 1.35203404799555e-5*x**2
        + 0.00357538393743079*x + 0.085
        )/(
        4.74334912634438e-11*x**4 + 4.09576274286244e-6*x**3
        + 0.00334241812250921*x**2 + 0.15406018058983*x + 1.0
    )

    expected = (
        133.599202650992/(x + 85524.0054884464)
        + 1.07757928431867/(x + 774.88576677949)
        + 0.395006955518971/(x + 40.7977016133126)
        + 0.564264854137341/(x + 7.79746609204661)
    )

    f_apart = apart(f, full=True).evalf()

    # There is a significant floating point error in this operation.
    assert all_close(f_apart, expected, rtol=1e-3, atol=1e-5)

