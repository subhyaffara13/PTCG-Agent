
def test_noncommutative_expand_issue_3757():
    A, B, C = symbols('A,B,C', commutative=False)
    assert A*B - B*A != 0
    assert (A*(A + B)*B).expand() == A**2*B + A*B**2
    assert (A*(A + B + C)*B).expand() == A**2*B + A*B**2 + A*C*B

