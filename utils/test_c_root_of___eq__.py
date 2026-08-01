
def test_CRootOf___eq__():
    assert (rootof(x**3 + x + 3, 0) == rootof(x**3 + x + 3, 0)) is True
    assert (rootof(x**3 + x + 3, 0) == rootof(x**3 + x + 3, 1)) is False
    assert (rootof(x**3 + x + 3, 1) == rootof(x**3 + x + 3, 1)) is True
    assert (rootof(x**3 + x + 3, 1) == rootof(x**3 + x + 3, 2)) is False
    assert (rootof(x**3 + x + 3, 2) == rootof(x**3 + x + 3, 2)) is True

    assert (rootof(x**3 + x + 3, 0) == rootof(y**3 + y + 3, 0)) is True
    assert (rootof(x**3 + x + 3, 0) == rootof(y**3 + y + 3, 1)) is False
    assert (rootof(x**3 + x + 3, 1) == rootof(y**3 + y + 3, 1)) is True
    assert (rootof(x**3 + x + 3, 1) == rootof(y**3 + y + 3, 2)) is False
    assert (rootof(x**3 + x + 3, 2) == rootof(y**3 + y + 3, 2)) is True

