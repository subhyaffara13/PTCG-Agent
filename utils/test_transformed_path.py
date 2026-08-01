
def test_transformed_path():
    points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    path = Path(points, closed=True)

    trans = mtransforms.Affine2D()
    trans_path = mtransforms.TransformedPath(path, trans)
    assert_allclose(trans_path.get_fully_transformed_path().vertices, points)

    # Changing the transform should change the result.
    r2 = 1 / np.sqrt(2)
    trans.rotate(np.pi / 4)
    assert_allclose(trans_path.get_fully_transformed_path().vertices,
                    [(0, 0), (r2, r2), (0, 2 * r2), (-r2, r2)],
                    atol=1e-15)

