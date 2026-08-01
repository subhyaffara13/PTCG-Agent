
def test_lambdify_transl():
    from sympy.utilities.lambdify import NUMPY_TRANSLATIONS
    for sym, mat in NUMPY_TRANSLATIONS.items():
        assert sym in sympy.__dict__
        assert mat in numpy.__dict__

