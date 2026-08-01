
def test_gcdext():
    assert gcdext(0, 0) == (0, 0, 0)
    assert gcdext(3, 0) == (3, 1, 0)
    assert gcdext(0, 4) == (4, 0, 1)

    for n in range(1, 10):
        assert gcdext(n, 1) == gcdext(-n, 1) == (1, 0, 1)
        assert gcdext(n, -1) == gcdext(-n, -1) == (1, 0, -1)
        assert gcdext(n, n) == gcdext(-n, n) == (n, 0, 1)
        assert gcdext(n, -n) == gcdext(-n, -n) == (n, 0, -1)

    for n in range(2, 10):
        assert gcdext(1, n) == gcdext(1, -n) == (1, 1, 0)
        assert gcdext(-1, n) == gcdext(-1, -n) == (1, -1, 0)

    for a, b in permutations([2**5, 3, 5, 7**2, 11], 2):
        g, x, y = gcdext(a, b)
        assert g == a*x + b*y == 1

