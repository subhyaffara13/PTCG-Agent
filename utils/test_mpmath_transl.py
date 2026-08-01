
def test_mpmath_transl():
    from sympy.utilities.lambdify import MPMATH_TRANSLATIONS
    for sym, mat in MPMATH_TRANSLATIONS.items():
        assert sym in sympy.__dict__ or sym == 'Matrix'
        assert mat in mpmath.__dict__

