
def test_issue_21758():
    from sympy.functions.elementary.piecewise import piecewise_fold
    from sympy.series.fourier import FourierSeries
    x = Symbol('x')
    k, n = symbols('k n')
    fo = FourierSeries(x, (x, -pi, pi), (0, SeqFormula(0, (k, 1, oo)), SeqFormula(
        Piecewise((-2*pi*cos(n*pi)/n + 2*sin(n*pi)/n**2, (n > -oo) & (n < oo) & Ne(n, 0)),
                  (0, True))*sin(n*x)/pi, (n, 1, oo))))
    assert latex(piecewise_fold(fo)) == '\\begin{cases} 2 \\sin{\\left(x \\right)}' \
            ' - \\sin{\\left(2 x \\right)} + \\frac{2 \\sin{\\left(3 x \\right)}}{3} +' \
            ' \\ldots & \\text{for}\\: n > -\\infty \\wedge n < \\infty \\wedge ' \
                'n \\neq 0 \\\\0 & \\text{otherwise} \\end{cases}'
    assert latex(FourierSeries(x, (x, -pi, pi), (0, SeqFormula(0, (k, 1, oo)),
                                                 SeqFormula(0, (n, 1, oo))))) == '0'


def test_issue_21758():
    from sympy.functions.elementary.piecewise import piecewise_fold
    from sympy.series.fourier import FourierSeries
    x = Symbol('x')
    k, n = symbols('k n')
    fo = FourierSeries(x, (x, -pi, pi), (0, SeqFormula(0, (k, 1, oo)), SeqFormula(
        Piecewise((-2*pi*cos(n*pi)/n + 2*sin(n*pi)/n**2, (n > -oo) & (n < oo) & Ne(n, 0)),
                  (0, True))*sin(n*x)/pi, (n, 1, oo))))
    assert upretty(piecewise_fold(fo)) == \
        '⎧                      2⋅sin(3⋅x)                                \n'\
        '⎪2⋅sin(x) - sin(2⋅x) + ────────── + …  for n > -∞ ∧ n < ∞ ∧ n ≠ 0\n'\
        '⎨                          3                                     \n'\
        '⎪                                                                \n'\
        '⎩                 0                            otherwise         '
    assert pretty(FourierSeries(x, (x, -pi, pi), (0, SeqFormula(0, (k, 1, oo)),
                                                 SeqFormula(0, (n, 1, oo))))) == '0'

