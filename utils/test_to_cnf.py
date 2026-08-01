
def test_to_cnf():
    assert to_cnf(~(B | C)) == And(Not(B), Not(C))
    assert to_cnf((A & B) | C) == And(Or(A, C), Or(B, C))
    assert to_cnf(A >> B) == (~A) | B
    assert to_cnf(A >> (B & C)) == (~A | B) & (~A | C)
    assert to_cnf(A & (B | C) | ~A & (B | C), True) == B | C
    assert to_cnf(A & B) == And(A, B)

    assert to_cnf(Equivalent(A, B)) == And(Or(A, Not(B)), Or(B, Not(A)))
    assert to_cnf(Equivalent(A, B & C)) == \
           (~A | B) & (~A | C) & (~B | ~C | A)
    assert to_cnf(Equivalent(A, B | C), True) == \
           And(Or(Not(B), A), Or(Not(C), A), Or(B, C, Not(A)))
    assert to_cnf(A + 1) == A + 1


def test_to_CNF():
    assert CNF.CNF_to_cnf(CNF.to_CNF(~(B | C))) == to_cnf(~(B | C))
    assert CNF.CNF_to_cnf(CNF.to_CNF((A & B) | C)) == to_cnf((A & B) | C)
    assert CNF.CNF_to_cnf(CNF.to_CNF(A >> B)) == to_cnf(A >> B)
    assert CNF.CNF_to_cnf(CNF.to_CNF(A >> (B & C))) == to_cnf(A >> (B & C))
    assert CNF.CNF_to_cnf(CNF.to_CNF(A & (B | C) | ~A & (B | C))) == to_cnf(A & (B | C) | ~A & (B | C))
    assert CNF.CNF_to_cnf(CNF.to_CNF(A & B)) == to_cnf(A & B)

