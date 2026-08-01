
def test_reset_bounds():
    bf = Q.ge(x, 1) & Q.lt(x, 1)
    enc = boolean_formula_to_encoded_cnf(bf)
    lra, _ = LRASolver.from_encoded_cnf(enc, testing_mode=True)
    for clause in enc.data:
        for lit in clause:
            lra.assert_lit(lit)
    assert len(lra.enc_to_boundary) == 2
    assert lra.check()[0] == False

    lra.reset_bounds()
    assert lra.check()[0] == True
    for var in lra.all_var:
        assert var.upper == LRARational(float("inf"), 0)
        assert var.upper_from_eq == False
        assert var.upper_from_neg == False
        assert var.lower == LRARational(-float("inf"), 0)
        assert var.lower_from_eq == False
        assert var.lower_from_neg == False
        assert var.assign == LRARational(0, 0)
        assert var.var is not None
        assert var.col_idx is not None

