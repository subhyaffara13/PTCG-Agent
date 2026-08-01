
def test_pos_neg_infinite():
    bf = Q.positive_infinite(x) & Q.lt(x, 10000000) & Q.positive_infinite(y)
    enc = boolean_formula_to_encoded_cnf(bf)
    lra, _ = LRASolver.from_encoded_cnf(enc, testing_mode=True)
    for lit in enc.encoding.values():
        if lra.assert_lit(lit) is not None:
            break
    assert len(lra.enc_to_boundary) == 3
    assert lra.check()[0] == False

    bf = Q.positive_infinite(x) & Q.gt(x, 10000000) & Q.positive_infinite(y)
    enc = boolean_formula_to_encoded_cnf(bf)
    lra, _ = LRASolver.from_encoded_cnf(enc, testing_mode=True)
    for lit in enc.encoding.values():
        if lra.assert_lit(lit) is not None:
            break
    assert len(lra.enc_to_boundary) == 3
    assert lra.check()[0] == True

    bf = Q.positive_infinite(x) & Q.negative_infinite(x)
    enc = boolean_formula_to_encoded_cnf(bf)
    lra, _ = LRASolver.from_encoded_cnf(enc, testing_mode=True)
    for lit in enc.encoding.values():
        if lra.assert_lit(lit) is not None:
            break
    assert len(lra.enc_to_boundary) == 2
    assert lra.check()[0] == False

