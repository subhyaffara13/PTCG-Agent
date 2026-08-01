
def test_to_nnf():
    assert to_nnf(true) is true
    assert to_nnf(false) is false
    assert to_nnf(A) == A
    assert to_nnf(A | ~A | B) is true
    assert to_nnf(A & ~A & B) is false
    assert to_nnf(A >> B) == ~A | B
    assert to_nnf(Equivalent(A, B, C)) == (~A | B) & (~B | C) & (~C | A)
    assert to_nnf(A ^ B ^ C) == \
           (A | B | C) & (~A | ~B | C) & (A | ~B | ~C) & (~A | B | ~C)
    assert to_nnf(ITE(A, B, C)) == (~A | B) & (A | C)
    assert to_nnf(Not(A | B | C)) == ~A & ~B & ~C
    assert to_nnf(Not(A & B & C)) == ~A | ~B | ~C
    assert to_nnf(Not(A >> B)) == A & ~B
    assert to_nnf(Not(Equivalent(A, B, C))) == And(Or(A, B, C), Or(~A, ~B, ~C))
    assert to_nnf(Not(A ^ B ^ C)) == \
           (~A | B | C) & (A | ~B | C) & (A | B | ~C) & (~A | ~B | ~C)
    assert to_nnf(Not(ITE(A, B, C))) == (~A | ~B) & (A | ~C)
    assert to_nnf((A >> B) ^ (B >> A)) == (A & ~B) | (~A & B)
    assert to_nnf((A >> B) ^ (B >> A), False) == \
           (~A | ~B | A | B) & ((A & ~B) | (~A & B))
    assert ITE(A, 1, 0).to_nnf() == A
    assert ITE(A, 0, 1).to_nnf() == ~A
    # although ITE can hold non-Boolean, it will complain if
    # an attempt is made to convert the ITE to Boolean nnf
    raises(TypeError, lambda: ITE(A < 1, [1], B).to_nnf())

