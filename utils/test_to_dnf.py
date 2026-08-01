
def test_to_dnf():
    assert to_dnf(~(B | C)) == And(Not(B), Not(C))
    assert to_dnf(A & (B | C)) == Or(And(A, B), And(A, C))
    assert to_dnf(A >> B) == (~A) | B
    assert to_dnf(A >> (B & C)) == (~A) | (B & C)
    assert to_dnf(A | B) == A | B

    assert to_dnf(Equivalent(A, B), True) == \
           Or(And(A, B), And(Not(A), Not(B)))
    assert to_dnf(Equivalent(A, B & C), True) == \
           Or(And(A, B, C), And(Not(A), Not(B)), And(Not(A), Not(C)))
    assert to_dnf(A + 1) == A + 1

