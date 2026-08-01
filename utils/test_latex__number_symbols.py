
def test_latex_NumberSymbols():
    assert latex(S.Catalan) == "G"
    assert latex(S.EulerGamma) == r"\gamma"
    assert latex(S.Exp1) == "e"
    assert latex(S.GoldenRatio) == r"\phi"
    assert latex(S.Pi) == r"\pi"
    assert latex(S.TribonacciConstant) == r"\text{TribonacciConstant}"

