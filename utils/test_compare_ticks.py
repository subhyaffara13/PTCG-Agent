
def test_compare_ticks(cls):
    three = cls(3)
    four = cls(4)

    assert three < cls(4)
    assert cls(3) < four
    assert four > cls(3)
    assert cls(4) > three
    assert cls(3) == cls(3)
    assert cls(3) != cls(4)

