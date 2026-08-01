
def test_latex_ordinals():
    w = OrdinalOmega()
    assert latex(w) == r"\omega"
    wp = OmegaPower(2, 3)
    assert latex(wp) == r'3 \omega^{2}'
    assert latex(Ordinal(wp, OmegaPower(1, 1))) == r'3 \omega^{2} + \omega'
    assert latex(Ordinal(OmegaPower(2, 1), OmegaPower(1, 2))) == r'\omega^{2} + 2 \omega'

