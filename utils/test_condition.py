
def test_condition():
    rl = condition(lambda x: x % 2 == 0, posdec)
    assert rl(5) == 5
    assert rl(4) == 3


def test_condition():
    brl = condition(even, branch5)
    assert set(brl(4)) == set(branch5(4))
    assert set(brl(5)) == set()

