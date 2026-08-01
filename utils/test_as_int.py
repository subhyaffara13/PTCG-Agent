
def test_as_int():
    raises(ValueError, lambda : as_int(True))
    raises(ValueError, lambda : as_int(1.1))
    raises(ValueError, lambda : as_int([]))
    raises(ValueError, lambda : as_int(S.NaN))
    raises(ValueError, lambda : as_int(S.Infinity))
    raises(ValueError, lambda : as_int(S.NegativeInfinity))
    raises(ValueError, lambda : as_int(S.ComplexInfinity))
    # for the following, limited precision makes int(arg) == arg
    # but the int value is not necessarily what a user might have
    # expected; Q.prime is more nuanced in its response for
    # expressions which might be complex representations of an
    # integer. This is not -- by design -- as_ints role.
    raises(ValueError, lambda : as_int(1e23))
    raises(ValueError, lambda : as_int(S('1.'+'0'*20+'1')))
    assert as_int(True, strict=False) == 1

