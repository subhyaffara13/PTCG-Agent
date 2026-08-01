
def test_builtin_no_args():
    assert latex(Chi) == r'\operatorname{Chi}'
    assert latex(beta) == r'\operatorname{B}'
    assert latex(gamma) == r'\Gamma'
    assert latex(KroneckerDelta) == r'\delta'
    assert latex(DiracDelta) == r'\delta'
    assert latex(lowergamma) == r'\gamma'

