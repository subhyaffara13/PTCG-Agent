
def test_PolyRing_add():
    R, x = ring("x", ZZ)
    F = [ x**2 + 2*i + 3 for i in range(4) ]

    assert R.add(F) == reduce(add, F) == 4*x**2 + 24

    R, = ring("", ZZ)

    assert R.add([2, 5, 7]) == 14

