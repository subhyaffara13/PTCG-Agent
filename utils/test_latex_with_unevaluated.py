
def test_latex_with_unevaluated():
    with evaluate(False):
        assert latex(a * a) == r"a a"

