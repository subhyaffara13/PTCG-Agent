
def test_negation():
    assert HANDLE_NEGATION is True
    bf = Q.gt(x, 1) & ~Q.gt(x, 0)
    enc = boolean_formula_to_encoded_cnf(bf)
    lra, _ = LRASolver.from_encoded_cnf(enc, testing_mode=True)
    for clause in enc.data:
        for lit in clause:
            lra.assert_lit(lit)
    assert len(lra.enc_to_boundary) == 2
    assert lra.check()[0] == False
    assert sorted(lra.check()[1]) in [[-1, 2], [-2, 1]]

    bf = ~Q.gt(x, 1) & ~Q.lt(x, 0)
    enc = boolean_formula_to_encoded_cnf(bf)
    lra, _ = LRASolver.from_encoded_cnf(enc, testing_mode=True)
    for clause in enc.data:
        for lit in clause:
            lra.assert_lit(lit)
    assert len(lra.enc_to_boundary) == 2
    assert lra.check()[0] == True

    bf = ~Q.gt(x, 0) & ~Q.lt(x, 1)
    enc = boolean_formula_to_encoded_cnf(bf)
    lra, _ = LRASolver.from_encoded_cnf(enc, testing_mode=True)
    for clause in enc.data:
        for lit in clause:
            lra.assert_lit(lit)
    assert len(lra.enc_to_boundary) == 2
    assert lra.check()[0] == False

    bf = ~Q.gt(x, 0) & ~Q.le(x, 0)
    enc = boolean_formula_to_encoded_cnf(bf)
    lra, _ = LRASolver.from_encoded_cnf(enc, testing_mode=True)
    for clause in enc.data:
        for lit in clause:
            lra.assert_lit(lit)
    assert len(lra.enc_to_boundary) == 2
    assert lra.check()[0] == False

    bf = ~Q.le(x+y, 2) & ~Q.ge(x-y, 2) & ~Q.ge(y, 0)
    enc = boolean_formula_to_encoded_cnf(bf)
    lra, _ = LRASolver.from_encoded_cnf(enc, testing_mode=True)
    for clause in enc.data:
        for lit in clause:
            lra.assert_lit(lit)
    assert len(lra.enc_to_boundary) == 3
    assert lra.check()[0] == False
    assert len(lra.check()[1]) == 3
    assert all(i > 0 for i in lra.check()[1])


def test_negation():
    assert -S.Zero is S.Zero
    assert -Float(0) is not S.Zero and -Float(0) == 0.0

