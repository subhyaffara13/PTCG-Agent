
def test_global_settings():
    import inspect

    # settings should be visible in the signature of `latex`
    assert inspect.signature(latex).parameters['imaginary_unit'].default == r'i'
    assert latex(I) == r'i'
    try:
        # but changing the defaults...
        LatexPrinter.set_global_settings(imaginary_unit='j')
        # ... should change the signature
        assert inspect.signature(latex).parameters['imaginary_unit'].default == r'j'
        assert latex(I) == r'j'
    finally:
        # there's no public API to undo this, but we need to make sure we do
        # so as not to impact other tests
        del LatexPrinter._global_settings['imaginary_unit']

    # check we really did undo it
    assert inspect.signature(latex).parameters['imaginary_unit'].default == r'i'
    assert latex(I) == r'i'

