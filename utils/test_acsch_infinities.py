
def test_acsch_infinities():
    assert acsch(oo) == 0
    assert acsch(-oo) == 0
    assert acsch(zoo) == 0

