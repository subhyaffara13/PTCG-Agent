
def test_PolyRing_ring_new():
    R, x, y, z = ring("x,y,z", QQ)

    assert R.ring_new(7) == R(7)
    assert R.ring_new(7*x*y*z) == 7*x*y*z

    f = x**2 + 2*x*y + 3*x + 4*z**2 + 5*z + 6

    assert R.ring_new([[[1]], [[2], [3]], [[4, 5, 6]]]) == f
    assert R.ring_new({(2, 0, 0): 1, (1, 1, 0): 2, (1, 0, 0): 3, (0, 0, 2): 4, (0, 0, 1): 5, (0, 0, 0): 6}) == f
    assert R.ring_new([((2, 0, 0), 1), ((1, 1, 0), 2), ((1, 0, 0), 3), ((0, 0, 2), 4), ((0, 0, 1), 5), ((0, 0, 0), 6)]) == f

    R, = ring("", QQ)
    assert R.ring_new([((), 7)]) == R(7)

