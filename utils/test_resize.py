
def test_resize():
    p = Permutation(0, 1, 2)
    assert p.resize(5) == Permutation(0, 1, 2, size=5)
    assert p.resize(4) == Permutation(0, 1, 2, size=4)
    assert p.resize(3) == p
    raises(ValueError, lambda: p.resize(2))

    p = Permutation(0, 1, 2)(3, 4)(5, 6)
    assert p.resize(3) == Permutation(0, 1, 2)
    raises(ValueError, lambda: p.resize(4))

