
def test_from_encoded_cnf():
    s1, s2 = symbols("s1 s2")

    # Test preprocessing
    # Example is from section 3 of paper.
    phi = (x >= 0) & ((x + y <= 2) | (x + 2 * y - z >= 6)) & (Eq(x + y, 2) | (x + 2 * y - z > 4))
    enc = boolean_formula_to_encoded_cnf(phi)
    lra, _ = LRASolver.from_encoded_cnf(enc, testing_mode=True)
    assert lra.A.shape == (2, 5)
    assert str(lra.slack) == '[_s1, _s2]'
    assert str(lra.nonslack) == '[x, y, z]'
    assert lra.A == Matrix([[ 1,  1, 0, -1,  0],
                            [-1, -2, 1,  0, -1]])
    assert {(str(b.var), b.bound, b.upper, b.equality, b.strict) for b in lra.enc_to_boundary.values()} == {('_s1', 2, None, True, False),
    ('_s1', 2, True, False, False),
    ('_s2', -4, True, False, True),
    ('_s2', -6, True, False, False),
    ('x', 0, False, False, False)}

