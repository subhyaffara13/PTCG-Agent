
def test_mapparms(Poly):
    # check with defaults. Should be identity.
    d = Poly.domain
    w = Poly.window
    p = Poly([1], domain=d, window=w)
    assert_almost_equal([0, 1], p.mapparms())
    #
    w = 2 * d + 1
    p = Poly([1], domain=d, window=w)
    assert_almost_equal([1, 2], p.mapparms())

