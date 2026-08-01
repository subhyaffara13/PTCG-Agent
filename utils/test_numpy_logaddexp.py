
def test_numpy_logaddexp():
    lae = logaddexp(a, b)
    assert NumPyPrinter().doprint(lae) == 'numpy.logaddexp(a, b)'
    lae2 = logaddexp2(a, b)
    assert NumPyPrinter().doprint(lae2) == 'numpy.logaddexp2(a, b)'

