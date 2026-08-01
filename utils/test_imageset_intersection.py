
def test_imageset_intersection():
    n = Dummy()
    s = ImageSet(Lambda(n, -I*(I*(2*pi*n - pi/4) +
        log(Abs(sqrt(-I))))), S.Integers)
    assert s.intersect(S.Reals) == ImageSet(
        Lambda(n, 2*pi*n + pi*Rational(7, 4)), S.Integers)

