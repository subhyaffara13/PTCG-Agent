
def test_latex_Float():
    assert latex(Float(1.0e100)) == r"1.0 \cdot 10^{100}"
    assert latex(Float(1.0e-100)) == r"1.0 \cdot 10^{-100}"
    assert latex(Float(1.0e-100), mul_symbol="times") == \
        r"1.0 \times 10^{-100}"
    assert latex(Float('10000.0'), full_prec=False, min=-2, max=2) == \
        r"1.0 \cdot 10^{4}"
    assert latex(Float('10000.0'), full_prec=False, min=-2, max=4) == \
        r"1.0 \cdot 10^{4}"
    assert latex(Float('10000.0'), full_prec=False, min=-2, max=5) == \
        r"10000.0"
    assert latex(Float('0.099999'), full_prec=True,  min=-2, max=5) == \
        r"9.99990000000000 \cdot 10^{-2}"

