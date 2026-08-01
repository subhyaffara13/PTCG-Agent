
def test_issue_17382():
    # copied from sympy/core/tests/test_evalf.py
    def NS(e, n=15, **options):
        return sstr(sympify(e).evalf(n, **options), full_prec=True)

    x = Symbol('x')
    expr = solveset(2 * cos(x) * cos(2 * x) - 1, x, S.Reals)
    expected = "Union(" \
               "ImageSet(Lambda(_n, 6.28318530717959*_n + 5.79812359592087), Integers), " \
               "ImageSet(Lambda(_n, 6.28318530717959*_n + 0.485061711258717), Integers))"
    assert NS(expr) == expected

