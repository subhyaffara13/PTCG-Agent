
def test_is_nnf():
    assert is_nnf(true) is True
    assert is_nnf(A) is True
    assert is_nnf(~A) is True
    assert is_nnf(A & B) is True
    assert is_nnf((A & B) | (~A & A) | (~B & B) | (~A & ~B), False) is True
    assert is_nnf((A | B) & (~A | ~B)) is True
    assert is_nnf(Not(Or(A, B))) is False
    assert is_nnf(A ^ B) is False
    assert is_nnf((A & B) | (~A & A) | (~B & B) | (~A & ~B), True) is False

