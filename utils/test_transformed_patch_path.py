
def test_transformed_patch_path():
    trans = mtransforms.Affine2D()
    patch = mpatches.Wedge((0, 0), 1, 45, 135, transform=trans)

    tpatch = mtransforms.TransformedPatchPath(patch)
    points = tpatch.get_fully_transformed_path().vertices

    # Changing the transform should change the result.
    trans.scale(2)
    assert_allclose(tpatch.get_fully_transformed_path().vertices, points * 2)

    # Changing the path should change the result (and cancel out the scaling
    # from the transform).
    patch.set_radius(0.5)
    assert_allclose(tpatch.get_fully_transformed_path().vertices, points)

