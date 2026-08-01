
def test_cutdeg(Poly):
    p = Poly([1, 2, 3])
    assert_raises(ValueError, p.cutdeg, .5)
    assert_raises(ValueError, p.cutdeg, -1)
    assert_equal(len(p.cutdeg(3)), 3)
    assert_equal(len(p.cutdeg(2)), 3)
    assert_equal(len(p.cutdeg(1)), 2)
    assert_equal(len(p.cutdeg(0)), 1)

