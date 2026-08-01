
def test_eliminate_implications():
    assert eliminate_implications(Implies(A, B, evaluate=False)) == (~A) | B
    assert eliminate_implications(
        A >> (C >> Not(B))) == Or(Or(Not(B), Not(C)), Not(A))
    assert eliminate_implications(Equivalent(A, B, C, D)) == \
           (~A | B) & (~B | C) & (~C | D) & (~D | A)

