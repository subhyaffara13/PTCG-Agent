
def test_proper_divisors_and_proper_divisor_count():
    assert proper_divisors(-1) == []
    assert proper_divisors(0) == []
    assert proper_divisors(1) == []
    assert proper_divisors(2) == [1]
    assert proper_divisors(3) == [1]
    assert proper_divisors(17) == [1]
    assert proper_divisors(10) == [1, 2, 5]
    assert proper_divisors(100) == [1, 2, 4, 5, 10, 20, 25, 50]
    assert proper_divisors(1000000007) == [1]
    assert type(proper_divisors(2, generator=True)) is not list

    assert proper_divisor_count(0) == 0
    assert proper_divisor_count(-1) == 0
    assert proper_divisor_count(1) == 0
    assert proper_divisor_count(36) == 8
    assert proper_divisor_count(2*3*5) == 7

