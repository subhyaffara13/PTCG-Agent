
def test_sympify_mpmath():
    value = sympify(mpmath.mpf(1.0))
    assert value == Float(1.0) and type(value) is Float

    mpmath.mp.dps = 12
    assert sympify(
        mpmath.pi).epsilon_eq(Float("3.14159265359"), Float("1e-12")) == True
    assert sympify(
        mpmath.pi).epsilon_eq(Float("3.14159265359"), Float("1e-13")) == False

    mpmath.mp.dps = 6
    assert sympify(
        mpmath.pi).epsilon_eq(Float("3.14159"), Float("1e-5")) == True
    assert sympify(
        mpmath.pi).epsilon_eq(Float("3.14159"), Float("1e-6")) == False

    mpmath.mp.dps = 15
    assert sympify(mpmath.mpc(1.0 + 2.0j)) == Float(1.0) + Float(2.0)*I

