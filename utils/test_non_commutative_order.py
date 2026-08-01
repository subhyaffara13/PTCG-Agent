
def test_non_commutative_order():
    A, B, C = symbols('A B C', commutative=False)
    x0 = symbols('x0', commutative=False)
    l = [B+C, A*(B+C)]
    assert cse(l) == ([(x0, B+C)], [x0, A*x0])

