
def test_triangulation_set_mask():
    x = [-1, 0, 1, 0]
    y = [0, -1, 0, 1]
    triangles = [[0, 1, 2], [2, 3, 0]]
    triang = mtri.Triangulation(x, y, triangles)

    # Check neighbors, which forces creation of C++ triangulation
    assert_array_equal(triang.neighbors, [[-1, -1, 1], [-1, -1, 0]])

    # Set mask
    triang.set_mask([False, True])
    assert_array_equal(triang.mask, [False, True])

    # Reset mask
    triang.set_mask(None)
    assert triang.mask is None

    msg = r"mask array must have same length as triangles array"
    for mask in ([False, True, False], [False], [True], False, True):
        with pytest.raises(ValueError, match=msg):
            triang.set_mask(mask)

