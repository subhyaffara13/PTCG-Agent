
def test_affine_inverted_invalidated():
    # Ensure that the an affine transform is not declared valid on access
    point = [1.0, 1.0]
    t = mtransforms.Affine2D()

    assert_almost_equal(point, t.transform(t.inverted().transform(point)))
    # Change and access the transform
    t.translate(1.0, 1.0).get_matrix()
    assert_almost_equal(point, t.transform(t.inverted().transform(point)))

