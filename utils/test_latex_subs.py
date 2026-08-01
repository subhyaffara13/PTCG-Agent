
def test_latex_subs():
    assert latex(Subs(x*y, (x, y), (1, 2))) == r'\left. x y \right|_{\substack{ x=1\\ y=2 }}'

