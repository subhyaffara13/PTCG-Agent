
def test_symbolic_matrix_elements():
    n, m = symbols('n,m')
    s1 = BBra([n])
    s2 = BKet([m])
    o = B(0)
    e = apply_operators(s1*o*s2)
    assert e == sqrt(m)*KroneckerDelta(n, m - 1)

