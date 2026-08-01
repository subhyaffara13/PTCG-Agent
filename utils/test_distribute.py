
def test_distribute():
    class T1(Basic):
        pass

    class T2(Basic):
        pass

    distribute_t12 = distribute(T1, T2)
    assert distribute_t12(T1(S(1), S(2), T2(S(3), S(4)), S(5))) == \
        T2(T1(S(1), S(2), S(3), S(5)), T1(S(1), S(2), S(4), S(5)))
    assert distribute_t12(T1(S(1), S(2), S(3))) == T1(S(1), S(2), S(3))


def test_distribute():
    assert distribute_and_over_or(Or(And(A, B), C)) == And(Or(A, C), Or(B, C))
    assert distribute_or_over_and(And(A, Or(B, C))) == Or(And(A, B), And(A, C))
    assert distribute_xor_over_and(And(A, Xor(B, C))) == Xor(And(A, B), And(A, C))

