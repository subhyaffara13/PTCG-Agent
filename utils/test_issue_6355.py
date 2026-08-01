
def test_issue_6355():
    # This tests a bug in the Wang algorithm that occurred only with a very
    # specific set of random numbers.
    random_sequence = [-1, -1, 0, 0, 0, 0, -1, -1, 0, -1, 3, -1, 3, 3, 3, 3, -1, 3]

    R, x, y, z = ring("x,y,z", ZZ)
    f = 2*x**2 + y*z - y - z**2 + z

    assert R.dmp_zz_wang(f, seed=random_sequence) == [f]

