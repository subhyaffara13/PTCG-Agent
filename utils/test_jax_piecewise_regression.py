
def test_jax_piecewise_regression():
    """
    NumPyPrinter needs to print Piecewise()'s choicelist as a list to avoid
    breaking compatibility with numpy 1.8. This is not necessary in numpy 1.9+.
    See gh-9747 and gh-9749 for details.
    """
    printer = JaxPrinter()
    p = Piecewise((1, x < 0), (0, True))
    assert printer.doprint(p) == \
        'jax.numpy.select([jax.numpy.less(x, 0),True], [1,0], default=jax.numpy.nan)'
    assert printer.module_imports == {'jax.numpy': {'select', 'less', 'nan'}}

