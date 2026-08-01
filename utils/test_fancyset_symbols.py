
def test_fancyset_symbols():
    assert latex(S.Rationals) == r'\mathbb{Q}'
    assert latex(S.Naturals) == r'\mathbb{N}'
    assert latex(S.Naturals0) == r'\mathbb{N}_0'
    assert latex(S.Integers) == r'\mathbb{Z}'
    assert latex(S.Reals) == r'\mathbb{R}'
    assert latex(S.Complexes) == r'\mathbb{C}'

