
def test_pretty_Contains():
    assert pretty(Contains(x, S.Integers)) == 'Contains(x, Integers)'
    assert upretty(Contains(x, S.Integers)) == 'x ∈ ℤ'

