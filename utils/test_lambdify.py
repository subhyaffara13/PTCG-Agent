
def test_lambdify():
    mpmath.mp.dps = 16
    sin02 = mpmath.mpf("0.198669330795061215459412627")
    f = lambdify(x, sin(x), "numpy")
    prec = 1e-15
    assert -prec < f(0.2) - sin02 < prec

    # if this succeeds, it can't be a numpy function

    if version_tuple(numpy.__version__) >= version_tuple('1.17'):
        with raises(TypeError):
            f(x)
    else:
        with raises(AttributeError):
            f(x)


def test_lambdify():
    try:
        from sympy import symbols, lambdify
        from numpy import __version__ as numversion
        if numversion < '2.4.0' and sys.hexversion == 0x30f00a3:
            return #NOTE: numpy Segfaults for the above combination
    except ImportError:
        return
    settings['recurse'] = True
    x = symbols("x")
    y = x**2
    f = lambdify([x], y)
    z = min
    d = globals()
    globalvars(f, recurse=True, builtin=True)
    assert z is min 
    assert d is globals() 

