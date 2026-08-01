
def test_gammas():
    assert upretty(lowergamma(x, y)) == "γ(x, y)"
    assert upretty(uppergamma(x, y)) == "Γ(x, y)"
    assert xpretty(gamma(x), use_unicode=True) == 'Γ(x)'
    assert xpretty(gamma, use_unicode=True) == 'Γ'
    assert xpretty(symbols('gamma', cls=Function)(x), use_unicode=True) == 'γ(x)'
    assert xpretty(symbols('gamma', cls=Function), use_unicode=True) == 'γ'

