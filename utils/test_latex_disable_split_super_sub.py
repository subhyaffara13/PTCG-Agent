
def test_latex_disable_split_super_sub():
    assert latex(Symbol('u^a_b')) == 'u^{a}_{b}'
    assert latex(Symbol('u^a_b'), disable_split_super_sub=False) == 'u^{a}_{b}'
    assert latex(Symbol('u^a_b'), disable_split_super_sub=True) == 'u\\^a\\_b'

