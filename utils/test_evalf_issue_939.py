
def test_evalf_issue_939():
    # https://github.com/sympy/sympy/issues/4038

    # The output form of an integral may differ by a step function between
    # revisions, making this test a bit useless. This can't be said about
    # other two tests. For now, all values of this evaluation are used here,
    # but in future this should be reconsidered.
    assert NS(integrate(1/(x**5 + 1), x).subs(x, 4), chop=True) in \
        ['-0.000976138910649103', '0.965906660135753', '1.93278945918216']

    assert NS(Integral(1/(x**5 + 1), (x, 2, 4))) == '0.0144361088886740'
    assert NS(
        integrate(1/(x**5 + 1), (x, 2, 4)), chop=True) == '0.0144361088886740'

