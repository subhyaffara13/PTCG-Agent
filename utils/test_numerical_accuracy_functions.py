
def test_numerical_accuracy_functions():
    prntr = SciPyPrinter()
    assert prntr.doprint(expm1(x)) == 'numpy.expm1(x)'
    assert prntr.doprint(log1p(x)) == 'numpy.log1p(x)'
    assert prntr.doprint(cosm1(x)) == 'scipy.special.cosm1(x)'

