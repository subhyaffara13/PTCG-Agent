
def test_which_real_roots():
    f = Poly(x**4 - 1)

    assert f.which_real_roots([1, -1]) == [1, -1]
    assert f.which_real_roots([1, -1, 2, 4]) == [1, -1]
    assert f.which_real_roots([1, -1, -1, 1, 2, 5]) == [1, -1]
    assert f.which_real_roots([10, 8, 7, -1, 1]) == [-1, 1]

    # no real roots
    # (technically its still a superset)
    f = Poly(x**2 + 1)
    assert f.which_real_roots([5, 10]) == []

    # not square free
    f = Poly((x-1)**2)
    assert f.which_real_roots([1, 1, -1, 2]) == [1]

    # candidates not superset
    f = Poly(x**2 - 1)
    assert f.which_real_roots([0, 2]) == [0, 2]

