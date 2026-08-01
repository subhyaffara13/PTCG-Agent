
def test_M13():
    n = Dummy('n')
    assert solveset_real(sin(x) - cos(x), x) == ImageSet(Lambda(n, n*pi - pi*R(7, 4)), S.Integers)

