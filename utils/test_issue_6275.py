
def test_issue_6275():
    x = Symbol('x')
    # both zero or both Muls...but neither "change would be very appreciated.
    # This is similar to x/x => 1 even though if x = 0, it is really nan.
    assert isinstance(x*0, type(0*S.Infinity))
    if 0*S.Infinity is S.NaN:
        b = Symbol('b', finite=None)
        assert (b*0).is_zero is None

