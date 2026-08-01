
def test_entails():
    A, B, C = symbols('A, B, C')
    assert entails(A, [A >> B, ~B]) is False
    assert entails(B, [Equivalent(A, B), A]) is True
    assert entails((A >> B) >> (~A >> ~B)) is False
    assert entails((A >> B) >> (~B >> ~A)) is True

