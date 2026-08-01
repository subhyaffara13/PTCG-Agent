
def test_transform_single_point():
    t = mtransforms.Affine2D()
    r = t.transform_affine((1, 1))
    assert r.shape == (2,)

