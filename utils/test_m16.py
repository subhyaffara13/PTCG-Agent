
def test_M16():
    n = Dummy('n')
    assert solveset(sin(x) - tan(x), x) == ImageSet(Lambda(n, n*pi), S.Integers)

