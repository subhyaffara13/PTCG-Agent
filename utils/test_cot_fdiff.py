
def test_cot_fdiff():
    assert cot(x).fdiff() == -cot(x)**2 - 1
    raises(ArgumentIndexError, lambda: cot(x).fdiff(2))

