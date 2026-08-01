
def test_interpolated_empty_path():
    path = Path(np.zeros((0, 2)))
    assert path.interpolated(42) is path

