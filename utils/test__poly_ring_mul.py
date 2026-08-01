
def test_PolyRing_mul():
    R, x = ring("x", ZZ)
    F = [ x**2 + 2*i + 3 for i in range(4) ]

    assert R.mul(F) == reduce(mul, F) == x**8 + 24*x**6 + 206*x**4 + 744*x**2 + 945

    R, = ring("", ZZ)

    assert R.mul([2, 3, 5]) == 30

