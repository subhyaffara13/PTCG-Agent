
def test_latex_DiracDelta():
    assert latex(DiracDelta(x)) == r"\delta\left(x\right)"
    assert latex(DiracDelta(x)**2) == r"\left(\delta\left(x\right)\right)^{2}"
    assert latex(DiracDelta(x, 0)) == r"\delta\left(x\right)"
    assert latex(DiracDelta(x, 5)) == \
        r"\delta^{\left( 5 \right)}\left( x \right)"
    assert latex(DiracDelta(x, 5)**2) == \
        r"\left(\delta^{\left( 5 \right)}\left( x \right)\right)^{2}"

