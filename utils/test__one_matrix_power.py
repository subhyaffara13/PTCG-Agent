
def test_OneMatrix_power():
    o = OneMatrix(3, 3)
    assert o ** 0 == Identity(3)
    assert o ** 1 == o
    assert o * o == o ** 2 == 3 * o
    assert o * o * o == o ** 3 == 9 * o

    o = OneMatrix(n, n)
    assert o * o == o ** 2 == n * o
    # powsimp necessary as n ** (n - 2) * n does not produce n ** (n - 1)
    assert powsimp(o ** (n - 1) * o) == o ** n == n ** (n - 1) * o

