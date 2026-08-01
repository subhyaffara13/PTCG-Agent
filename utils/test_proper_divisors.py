
def test_proper_divisors():
    assert proper_divisors(-1) == []
    assert proper_divisors(28) == [1, 2, 4, 7, 14]
    assert list(proper_divisors(3*5*7, True)) == [1, 3, 5, 15, 7, 21, 35]

