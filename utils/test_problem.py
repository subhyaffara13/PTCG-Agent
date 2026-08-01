
def test_problem():
    from sympy.logic.algorithms.lra_theory import LRASolver
    from sympy.assumptions.cnf import CNF, EncodedCNF
    cons = [-2 * x - 2 * y >= 7, -9 * y >= 7, -6 * y >= 5]
    cnf = CNF().from_prop(And(*cons))
    enc = EncodedCNF()
    enc.from_cnf(cnf)
    lra, _ = LRASolver.from_encoded_cnf(enc)
    lra.assert_lit(1)
    lra.assert_lit(2)
    lra.assert_lit(3)
    is_sat, assignment = lra.check()
    assert is_sat is True

