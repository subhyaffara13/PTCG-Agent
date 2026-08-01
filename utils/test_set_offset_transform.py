
def test_set_offset_transform():
    skew = mtransforms.Affine2D().skew(2, 2)
    init = mcollections.Collection(offset_transform=skew)

    late = mcollections.Collection()
    late.set_offset_transform(skew)

    assert skew == init.get_offset_transform() == late.get_offset_transform()

