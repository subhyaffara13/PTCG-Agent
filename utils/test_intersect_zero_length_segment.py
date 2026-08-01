
def test_intersect_zero_length_segment():
    this_path = Path(
        np.array([
            [0, 0],
            [1, 1],
        ]))

    outline_path = Path(
        np.array([
            [1, 0],
            [.5, .5],
            [.5, .5],
            [0, 1],
        ]))

    assert outline_path.intersects_path(this_path)
    assert this_path.intersects_path(outline_path)

