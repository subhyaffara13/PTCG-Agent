
def test_is_literal():
    assert is_literal(True) is True
    assert is_literal(False) is True
    assert is_literal(A) is True
    assert is_literal(~A) is True
    assert is_literal(Or(A, B)) is False
    assert is_literal(Q.zero(A)) is True
    assert is_literal(Not(Q.zero(A))) is True
    assert is_literal(Or(A, B)) is False
    assert is_literal(And(Q.zero(A), Q.zero(B))) is False
    assert is_literal(x < 3)
    assert not is_literal(x + y < 3)

