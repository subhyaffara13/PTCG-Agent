
def test_latex_AccumuBounds():
    a = Symbol('a', real=True)
    assert latex(AccumBounds(0, 1)) == r"\left\langle 0, 1\right\rangle"
    assert latex(AccumBounds(0, a)) == r"\left\langle 0, a\right\rangle"
    assert latex(AccumBounds(a + 1, a + 2)) == \
        r"\left\langle a + 1, a + 2\right\rangle"

