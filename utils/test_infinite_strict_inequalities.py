
def test_infinite_strict_inequalities():
    # Extensive testing of the interaction between strict inequalities
    # and constraints containing infinity is needed because
    # the paper's rule for strict inequalities don't work when
    # infinite numbers are allowed. Using the paper's rules you
    # can end up with situations where oo + delta > oo is considered
    # True when oo + delta should be equal to oo.
    # See https://math.stackexchange.com/questions/4757069/can-this-method-of-converting-strict-inequalities-to-equisatisfiable-nonstrict-i
    bf = (-x - y >= -float("inf")) & (x > 0) & (y >= float("inf"))
    enc = boolean_formula_to_encoded_cnf(bf)
    lra, _ = LRASolver.from_encoded_cnf(enc, testing_mode=True)
    for lit in sorted(enc.encoding.values()):
        if lra.assert_lit(lit) is not None:
            break
    assert len(lra.enc_to_boundary) == 3
    assert lra.check()[0] == True

