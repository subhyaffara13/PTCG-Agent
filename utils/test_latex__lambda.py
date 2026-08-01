
def test_latex_Lambda():
    assert latex(Lambda(x, x + 1)) == r"\left( x \mapsto x + 1 \right)"
    assert latex(Lambda((x, y), x + 1)) == r"\left( \left( x, \  y\right) \mapsto x + 1 \right)"
    assert latex(Lambda(x, x)) == r"\left( x \mapsto x \right)"

