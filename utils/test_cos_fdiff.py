
def test_cos_fdiff():
    assert cos(x).fdiff() == -sin(x)
    raises(ArgumentIndexError, lambda: cos(x).fdiff(2))

