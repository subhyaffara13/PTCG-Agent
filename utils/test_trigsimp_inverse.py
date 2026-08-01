
def test_trigsimp_inverse():
    alpha = symbols('alpha')
    s, c = sin(alpha), cos(alpha)

    for finv in [asin, acos, asec, acsc, atan, acot]:
        f = finv.inverse(None)
        assert alpha == trigsimp(finv(f(alpha)), inverse=True)

    # test atan2(cos, sin), atan2(sin, cos), etc...
    for a, b in [[c, s], [s, c]]:
        for i, j in product([-1, 1], repeat=2):
            angle = atan2(i*b, j*a)
            angle_inverted = trigsimp(angle, inverse=True)
            assert angle_inverted != angle  # assures simplification happened
            assert sin(angle_inverted) == trigsimp(sin(angle))
            assert cos(angle_inverted) == trigsimp(cos(angle))

