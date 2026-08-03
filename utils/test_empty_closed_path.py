from pathlib import Path


def test_empty_closed_path():
    path = Path(np.zeros((0, 2)), closed=True)
    assert path.vertices.shape == (0, 2)
    assert path.codes is None
    assert_array_equal(path.get_extents().extents,
                       transforms.Bbox.null().extents)

