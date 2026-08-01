
def test_udivisors_and_udivisor_count():
    assert udivisors(-1) == [1]
    assert udivisors(0) == []
    assert udivisors(1) == [1]
    assert udivisors(2) == [1, 2]
    assert udivisors(3) == [1, 3]
    assert udivisors(17) == [1, 17]
    assert udivisors(10) == [1, 2, 5, 10]
    assert udivisors(100) == [1, 4, 25, 100]
    assert udivisors(101) == [1, 101]
    assert udivisors(1000) == [1, 8, 125, 1000]
    assert type(udivisors(2, generator=True)) is not list

    assert udivisor_count(0) == 0
    assert udivisor_count(-1) == 1
    assert udivisor_count(1) == 1
    assert udivisor_count(6) == 4
    assert udivisor_count(12) == 4

    assert udivisor_count(180) == 8
    assert udivisor_count(2*3*5*7) == 16

