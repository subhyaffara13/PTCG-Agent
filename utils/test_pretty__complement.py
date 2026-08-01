
def test_pretty_Complement():
    assert pretty(S.Reals - S.Naturals) == '(-oo, oo) \\ Naturals'
    assert upretty(S.Reals - S.Naturals) == 'ℝ \\ ℕ'
    assert pretty(S.Reals - S.Naturals0) == '(-oo, oo) \\ Naturals0'
    assert upretty(S.Reals - S.Naturals0) == 'ℝ \\ ℕ₀'

