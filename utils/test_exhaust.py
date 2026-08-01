
def test_exhaust():
    sink = exhaust(posdec)
    assert sink(5) == 0
    assert sink(10) == 0


def test_exhaust():
    brl = exhaust(branch5)
    assert set(brl(3)) == {0}
    assert set(brl(7)) == {10}
    assert set(brl(5)) == {0, 10}

