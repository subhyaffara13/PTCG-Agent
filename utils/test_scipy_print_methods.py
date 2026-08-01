
def test_scipy_print_methods():
    prntr = SciPyPrinter()
    assert hasattr(prntr, '_print_acos')
    assert hasattr(prntr, '_print_log')
    assert hasattr(prntr, '_print_erf')
    assert hasattr(prntr, '_print_factorial')
    assert hasattr(prntr, '_print_chebyshevt')
    k = Symbol('k', integer=True, nonnegative=True)
    x = Symbol('x', real=True)
    assert prntr.doprint(polygamma(k, x)) == "scipy.special.polygamma(k, x)"
    assert prntr.doprint(Si(x)) == "scipy.special.sici(x)[0]"
    assert prntr.doprint(Ci(x)) == "scipy.special.sici(x)[1]"

