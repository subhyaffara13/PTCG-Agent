
def test_latex_Contains():
    x = Symbol('x')
    assert latex(Contains(x, S.Naturals)) == r"x \in \mathbb{N}"

