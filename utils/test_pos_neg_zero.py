
def test_pos_neg_zero():
    bf = Q.positive(x) & Q.negative(x) & Q.zero(y)
    enc = boolean_formula_to_encoded_cnf(bf)
    lra, _ = LRASolver.from_encoded_cnf(enc, testing_mode=True)
    for lit in enc.encoding.values():
        if lra.assert_lit(lit) is not None:
            break
    assert len(lra.enc_to_boundary) == 3
    assert lra.check()[0] == False

    bf = Q.positive(x) & Q.lt(x, -1)
    enc = boolean_formula_to_encoded_cnf(bf)
    lra, _ = LRASolver.from_encoded_cnf(enc, testing_mode=True)
    for lit in enc.encoding.values():
        if lra.assert_lit(lit) is not None:
            break
    assert len(lra.enc_to_boundary) == 2
    assert lra.check()[0] == False

    bf = Q.positive(x) & Q.zero(x)
    enc = boolean_formula_to_encoded_cnf(bf)
    lra, _ = LRASolver.from_encoded_cnf(enc, testing_mode=True)
    for lit in enc.encoding.values():
        if lra.assert_lit(lit) is not None:
            break
    assert len(lra.enc_to_boundary) == 2
    assert lra.check()[0] == False

    bf = Q.positive(x) & Q.zero(y)
    enc = boolean_formula_to_encoded_cnf(bf)
    lra, _ = LRASolver.from_encoded_cnf(enc, testing_mode=True)
    for lit in enc.encoding.values():
        if lra.assert_lit(lit) is not None:
            break
    assert len(lra.enc_to_boundary) == 2
    assert lra.check()[0] == True

