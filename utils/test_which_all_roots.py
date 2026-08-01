
def test_which_all_roots():
    f = Poly(x**4 - 1)

    assert f.which_all_roots([1, -1, I, -I]) == [1, -1, I, -I]
    assert f.which_all_roots([I, I, -I, 1, -1]) == [I, -I, 1, -1]

    f = Poly(x**2 + 1)
    assert f.which_all_roots([I, -I, I/2]) == [I, -I]

    # not square free
    f = Poly((x-I)**2)
    assert f.which_all_roots([I, I, 1, -1, 0]) == [I]

    # candidates not superset
    f = Poly(x**2 + 1)
    assert f.which_all_roots([I/2, -I/2]) == [I/2, -I/2]

