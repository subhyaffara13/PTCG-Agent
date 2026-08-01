
def test_latex_DFT_IDFT():
    from sympy.matrices.expressions.fourier import DFT, IDFT
    assert latex(DFT(13)) == r"\text{DFT}_{13}"
    assert latex(IDFT(x)) == r"\text{IDFT}_{x}"

