
def test_sec_fdiff():
    assert sec(x).fdiff() == tan(x)*sec(x)
    raises(ArgumentIndexError, lambda: sec(x).fdiff(2))

