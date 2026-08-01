
def test_numpy_piecewise_regression():
    """
    NumPyPrinter needs to print Piecewise()'s choicelist as a list to avoid
    breaking compatibility with numpy 1.8. This is not necessary in numpy 1.9+.
    See gh-9747 and gh-9749 for details.
    """
    printer = NumPyPrinter()
    p = Piecewise((1, x < 0), (0, True))
    assert printer.doprint(p) == \
        'numpy.select([numpy.less(x, 0),True], [1,0], default=numpy.nan)'
    assert printer.module_imports == {'numpy': {'select', 'less', 'nan'}}

