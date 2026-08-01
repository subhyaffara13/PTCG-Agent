
def test_M14():
    n = Dummy('n')
    assert solveset_real(tan(x) - 1, x) == ImageSet(Lambda(n, n*pi + pi/4), S.Integers)

