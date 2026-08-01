
def test_AccumBounds_exponent():
    # base is 0
    z = 0**B(a, a + S.Half)
    assert z.subs(a, 0) == B(0, 1)
    assert z.subs(a, 1) == 0
    p = z.subs(a, -1)
    assert p.is_Pow and p.args == (0, B(-1, -S.Half))
    # base > 0
    #   when base is 1 the type of bounds does not matter
    assert 1**B(a, a + 1) == 1
    #  otherwise we need to know if 0 is in the bounds
    assert S.Half**B(-2, 2) == B(S(1)/4, 4)
    assert 2**B(-2, 2) == B(S(1)/4, 4)

    # +eps may introduce +oo
    # if there is a negative integer exponent
    assert B(0, 1)**B(S(1)/2, 1) == B(0, 1)
    assert B(0, 1)**B(0, 1) == B(0, 1)

    # positive bases have positive bounds
    assert B(2, 3)**B(-3, -2) == B(S(1)/27, S(1)/4)
    assert B(2, 3)**B(-3, 2) == B(S(1)/27, 9)

    # bounds generating imaginary parts unevaluated
    assert unchanged(Pow, B(-1, 1), B(1, 2))
    assert B(0, S(1)/2)**B(1, oo) == B(0, S(1)/2)
    assert B(0, 1)**B(1, oo) == B(0, oo)
    assert B(0, 2)**B(1, oo) == B(0, oo)
    assert B(0, oo)**B(1, oo) == B(0, oo)
    assert B(S(1)/2, 1)**B(1, oo) == B(0, oo)
    assert B(S(1)/2, 1)**B(-oo, -1) == B(0, oo)
    assert B(S(1)/2, 1)**B(-oo, oo) == B(0, oo)
    assert B(S(1)/2, 2)**B(1, oo) == B(0, oo)
    assert B(S(1)/2, 2)**B(-oo, -1) == B(0, oo)
    assert B(S(1)/2, 2)**B(-oo, oo) == B(0, oo)
    assert B(S(1)/2, oo)**B(1, oo) == B(0, oo)
    assert B(S(1)/2, oo)**B(-oo, -1) == B(0, oo)
    assert B(S(1)/2, oo)**B(-oo, oo) == B(0, oo)
    assert B(1, 2)**B(1, oo) == B(0, oo)
    assert B(1, 2)**B(-oo, -1) == B(0, oo)
    assert B(1, 2)**B(-oo, oo) == B(0, oo)
    assert B(1, oo)**B(1, oo) == B(0, oo)
    assert B(1, oo)**B(-oo, -1) == B(0, oo)
    assert B(1, oo)**B(-oo, oo) == B(0, oo)
    assert B(2, oo)**B(1, oo) == B(2, oo)
    assert B(2, oo)**B(-oo, -1) == B(0, S(1)/2)
    assert B(2, oo)**B(-oo, oo) == B(0, oo)

