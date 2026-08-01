
def test_latex_limits():
    assert latex(Limit(x, x, oo)) == r"\lim_{x \to \infty} x"

    # issue 8175
    f = Function('f')
    assert latex(Limit(f(x), x, 0)) == r"\lim_{x \to 0^+} f{\left(x \right)}"
    assert latex(Limit(f(x), x, 0, "-")) == \
        r"\lim_{x \to 0^-} f{\left(x \right)}"

    # issue #10806
    assert latex(Limit(f(x), x, 0)**2) == \
        r"\left(\lim_{x \to 0^+} f{\left(x \right)}\right)^{2}"
    # bi-directional limit
    assert latex(Limit(f(x), x, 0, dir='+-')) == \
        r"\lim_{x \to 0} f{\left(x \right)}"

