
def test_satisfiable():
    A, B, C = symbols('A,B,C')
    assert satisfiable(A & (A >> B) & ~B) is False

