
def test_binrel_evaluation():
    bf = Q.gt(3, 2)
    enc = boolean_formula_to_encoded_cnf(bf)
    lra, conflicts = LRASolver.from_encoded_cnf(enc, testing_mode=True)
    assert len(lra.enc_to_boundary) == 0
    assert conflicts == [[1]]

    bf = Q.lt(3, 2)
    enc = boolean_formula_to_encoded_cnf(bf)
    lra, conflicts = LRASolver.from_encoded_cnf(enc, testing_mode=True)
    assert len(lra.enc_to_boundary) == 0
    assert conflicts == [[-1]]

