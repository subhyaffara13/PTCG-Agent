
def test_equals_None_vs_float():
    # GH#44190
    left = Series([-np.inf, np.nan, -1.0, 0.0, 1.0, 10 / 3, np.inf], dtype=object)
    right = Series([None] * len(left))

    # these series were found to be equal due to a bug, check that they are correctly
    # found to not equal
    assert not left.equals(right)
    assert not right.equals(left)
    assert not left.to_frame().equals(right.to_frame())
    assert not right.to_frame().equals(left.to_frame())
    assert not Index(left, dtype="object").equals(Index(right, dtype="object"))
    assert not Index(right, dtype="object").equals(Index(left, dtype="object"))

