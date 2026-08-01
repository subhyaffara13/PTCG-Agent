
def test_empty_cnf():
    cnf = CNF()
    enc = EncodedCNF()
    enc.from_cnf(cnf)
    lra, conflict = LRASolver.from_encoded_cnf(enc)
    assert len(conflict) == 0
    assert lra.check() == (True, {})

