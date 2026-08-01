
def test_divisors_and_divisor_count():
    assert divisors(-1) == [1]
    assert divisors(0) == []
    assert divisors(1) == [1]
    assert divisors(2) == [1, 2]
    assert divisors(3) == [1, 3]
    assert divisors(17) == [1, 17]
    assert divisors(10) == [1, 2, 5, 10]
    assert divisors(100) == [1, 2, 4, 5, 10, 20, 25, 50, 100]
    assert divisors(101) == [1, 101]
    assert type(divisors(2, generator=True)) is not list

    assert divisor_count(0) == 0
    assert divisor_count(-1) == 1
    assert divisor_count(1) == 1
    assert divisor_count(6) == 4
    assert divisor_count(12) == 6

    assert divisor_count(180, 3) == divisor_count(180//3)
    assert divisor_count(2*3*5, 7) == 0

