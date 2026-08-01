
def test_loc_with_positional_slice_raises():
    # GH#31840
    ser = Series(range(4), index=["A", "B", "C", "D"])

    with pytest.raises(TypeError, match="Slicing a positional slice with .loc"):
        ser.loc[:3] = 2

