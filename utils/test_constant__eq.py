
def test_constant_Eq():
    # C1 on the rhs is well-tested, but the lhs is only tested here
    assert constantsimp(Eq(C1, 3 + f(x)*x), [C1]) == Eq(x*f(x), C1)
    assert constantsimp(Eq(C1, 3 * f(x)*x), [C1]) == Eq(f(x)*x, C1)

