
def test_latex_Range():
    assert latex(Range(1, 51)) == r'\left\{1, 2, \ldots, 50\right\}'
    assert latex(Range(1, 4)) == r'\left\{1, 2, 3\right\}'
    assert latex(Range(0, 3, 1)) == r'\left\{0, 1, 2\right\}'
    assert latex(Range(0, 30, 1)) == r'\left\{0, 1, \ldots, 29\right\}'
    assert latex(Range(30, 1, -1)) == r'\left\{30, 29, \ldots, 2\right\}'
    assert latex(Range(0, oo, 2)) == r'\left\{0, 2, \ldots\right\}'
    assert latex(Range(oo, -2, -2)) == r'\left\{\ldots, 2, 0\right\}'
    assert latex(Range(-2, -oo, -1)) == r'\left\{-2, -3, \ldots\right\}'
    assert latex(Range(-oo, oo)) == r'\left\{\ldots, -1, 0, 1, \ldots\right\}'
    assert latex(Range(oo, -oo, -1)) == r'\left\{\ldots, 1, 0, -1, \ldots\right\}'

    a, b, c = symbols('a:c')
    assert latex(Range(a, b, c)) == r'\text{Range}\left(a, b, c\right)'
    assert latex(Range(a, 10, 1)) == r'\text{Range}\left(a, 10\right)'
    assert latex(Range(0, b, 1)) == r'\text{Range}\left(b\right)'
    assert latex(Range(0, 10, c)) == r'\text{Range}\left(0, 10, c\right)'

    i = Symbol('i', integer=True)
    n = Symbol('n', negative=True, integer=True)
    p = Symbol('p', positive=True, integer=True)

    assert latex(Range(i, i + 3)) == r'\left\{i, i + 1, i + 2\right\}'
    assert latex(Range(-oo, n, 2)) == r'\left\{\ldots, n - 4, n - 2\right\}'
    assert latex(Range(p, oo)) == r'\left\{p, p + 1, \ldots\right\}'
    # The following will work if __iter__ is improved
    # assert latex(Range(-3, p + 7)) == r'\left\{-3, -2,  \ldots, p + 6\right\}'
    # Must have integer assumptions
    assert latex(Range(a, a + 3)) == r'\text{Range}\left(a, a + 3\right)'

