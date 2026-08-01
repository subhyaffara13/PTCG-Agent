
def test_divisors():
    assert divisors(28) == [1, 2, 4, 7, 14, 28]
    assert list(divisors(3*5*7, 1)) == [1, 3, 5, 15, 7, 21, 35, 105]
    assert divisors(0) == []

