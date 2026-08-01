
def test_antidivisors():
    assert antidivisors(-1) == []
    assert antidivisors(-3) == [2]
    assert antidivisors(14) == [3, 4, 9]
    assert antidivisors(237) == [2, 5, 6, 11, 19, 25, 43, 95, 158]
    assert antidivisors(12345) == [2, 6, 7, 10, 30, 1646, 3527, 4938, 8230]
    assert antidivisors(393216) == [262144]
    assert sorted(x for x in antidivisors(3*5*7, 1)) == \
        [2, 6, 10, 11, 14, 19, 30, 42, 70]
    assert antidivisors(1) == []
    assert type(antidivisors(2, generator=True)) is not list

