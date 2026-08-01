
def test_validate_sketch(value):
    mpl.rcParams["path.sketch"] = value
    assert mpl.rcParams["path.sketch"] == (1, 2, 3)
    assert validate_sketch(value) == (1, 2, 3)

