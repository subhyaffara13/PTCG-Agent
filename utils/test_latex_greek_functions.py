
def test_latex_greek_functions():
    # bug because capital greeks that have roman equivalents should not use
    # \Alpha, \Beta, \Eta, etc.
    s = Function('Alpha')
    assert latex(s) == r'\mathrm{A}'
    assert latex(s(x)) == r'\mathrm{A}{\left(x \right)}'
    s = Function('Beta')
    assert latex(s) == r'\mathrm{B}'
    s = Function('Eta')
    assert latex(s) == r'\mathrm{H}'
    assert latex(s(x)) == r'\mathrm{H}{\left(x \right)}'

    # bug because sympy.core.numbers.Pi is special
    p = Function('Pi')
    # assert latex(p(x)) == r'\Pi{\left(x \right)}'
    assert latex(p) == r'\Pi'

    # bug because not all greeks are included
    c = Function('chi')
    assert latex(c(x)) == r'\chi{\left(x \right)}'
    assert latex(c) == r'\chi'

