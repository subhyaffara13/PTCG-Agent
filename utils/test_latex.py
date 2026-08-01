
def test_latex():
    assert latex((2*tau)**Rational(7, 2)) == r"8 \sqrt{2} \tau^{\frac{7}{2}}"
    assert latex((2*mu)**Rational(7, 2), mode='equation*') == \
        r"\begin{equation*}8 \sqrt{2} \mu^{\frac{7}{2}}\end{equation*}"
    assert latex((2*mu)**Rational(7, 2), mode='equation', itex=True) == \
        r"$$8 \sqrt{2} \mu^{\frac{7}{2}}$$"
    assert latex([2/x, y]) == r"\left[ \frac{2}{x}, \  y\right]"


def test_latex():
    assert latex(pi) == r"\pi"
    assert latex(E) == r"e"
    assert latex(GoldenRatio) == r"\phi"
    assert latex(TribonacciConstant) == r"\text{TribonacciConstant}"
    assert latex(EulerGamma) == r"\gamma"
    assert latex(oo) == r"\infty"
    assert latex(-oo) == r"-\infty"
    assert latex(zoo) == r"\tilde{\infty}"
    assert latex(nan) == r"\text{NaN}"
    assert latex(I) == r"i"

