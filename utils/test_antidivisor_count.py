
def test_antidivisor_count():
    assert antidivisor_count(0) == 0
    assert antidivisor_count(-1) == 0
    assert antidivisor_count(-4) == 1
    assert antidivisor_count(20) == 3
    assert antidivisor_count(25) == 5
    assert antidivisor_count(38) == 7
    assert antidivisor_count(180) == 6
    assert antidivisor_count(2*3*5) == 3

