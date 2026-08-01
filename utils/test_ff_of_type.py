
def test_FF_of_type():
    # XXX: of_type is not very useful here because in the case of ground types
    # = flint all elements are of type nmod.
    assert FF(3).of_type(FF(3)(1)) is True
    assert FF(5).of_type(FF(5)(3)) is True

