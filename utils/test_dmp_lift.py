
def test_dmp_lift():
    q = [QQ(1, 1), QQ(0, 1), QQ(1, 1)]

    f_a = [ANP([QQ(1, 1)], q, QQ), ANP([], q, QQ), ANP([], q, QQ),
         ANP([QQ(1, 1), QQ(0, 1)], q, QQ), ANP([QQ(17, 1), QQ(0, 1)], q, QQ)]

    f_lift = QQ.map([1, 0, 0, 0, 0, 0, 1, 34, 289])

    assert dmp_lift(f_a, 0, QQ.algebraic_field(I)) == f_lift

    f_g = [QQ_I(1), QQ_I(0), QQ_I(0), QQ_I(0, 1), QQ_I(0, 17)]

    assert dmp_lift(f_g, 0, QQ_I) == f_lift

    raises(DomainError, lambda: dmp_lift([EX(1), EX(2)], 0, EX))

