
def test_mul_noncommutative_mismatch():
    A, B, C = symbols('A B C', commutative=False)
    w = symbols('w', cls=Wild, commutative=False)

    assert (w*B*w).matches(A*B*A) == {w: A}
    assert (w*B*w).matches(A*C*B*A*C) == {w: A*C}
    assert (w*B*w).matches(A*C*B*A*B) is None
    assert (w*B*w).matches(A*B*C) is None
    assert (w*w*C).matches(A*B*C) is None

