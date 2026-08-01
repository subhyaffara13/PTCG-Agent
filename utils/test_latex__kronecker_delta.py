
def test_latex_KroneckerDelta():
    assert latex(KroneckerDelta(x, y)) == r"\delta_{x y}"
    assert latex(KroneckerDelta(x, y + 1)) == r"\delta_{x, y + 1}"
    # issue 6578
    assert latex(KroneckerDelta(x + 1, y)) == r"\delta_{y, x + 1}"
    assert latex(Pow(KroneckerDelta(x, y), 2, evaluate=False)) == \
        r"\left(\delta_{x y}\right)^{2}"

