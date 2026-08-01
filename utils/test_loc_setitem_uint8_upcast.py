
def test_loc_setitem_uint8_upcast(value):
    # GH#26049

    df = DataFrame([1, 2, 3, 4], columns=["col1"], dtype="uint8")
    with pytest.raises(TypeError, match="Invalid value"):
        df.loc[2, "col1"] = value  # value that can't be held in uint8

