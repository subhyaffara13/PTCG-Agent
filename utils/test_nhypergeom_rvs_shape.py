
def test_nhypergeom_rvs_shape():
    # Check that when given a size with more dimensions than the
    # dimensions of the broadcast parameters, rvs returns an array
    # with the correct shape.
    x = nhypergeom.rvs(22, [7, 8, 9], [[12], [13]], size=(5, 1, 2, 3))
    assert x.shape == (5, 1, 2, 3)

