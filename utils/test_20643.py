
def test_20643():
    # closed by GH#45121
    orig = Series([0, 1, 2], index=["a", "b", "c"])

    ser = orig.copy()
    with pytest.raises(TypeError, match="Invalid value"):
        ser.at["b"] = 2.7

    with pytest.raises(TypeError, match="Invalid value"):
        ser.loc["b"] = 2.7

    with pytest.raises(TypeError, match="Invalid value"):
        ser["b"] = 2.7

    ser = orig.copy()
    with pytest.raises(TypeError, match="Invalid value"):
        ser.iat[1] = 2.7

    with pytest.raises(TypeError, match="Invalid value"):
        ser.iloc[1] = 2.7

    orig_df = orig.to_frame("A")

    df = orig_df.copy()
    with pytest.raises(TypeError, match="Invalid value"):
        df.at["b", "A"] = 2.7

    with pytest.raises(TypeError, match="Invalid value"):
        df.loc["b", "A"] = 2.7

    with pytest.raises(TypeError, match="Invalid value"):
        df.iloc[1, 0] = 2.7

    with pytest.raises(TypeError, match="Invalid value"):
        df.iat[1, 0] = 2.7

