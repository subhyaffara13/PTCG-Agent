
def test_15413():
    # fixed by GH#45121
    ser = Series([1, 2, 3])

    with pytest.raises(TypeError, match="Invalid value"):
        ser[ser == 2] += 0.5

    with pytest.raises(TypeError, match="Invalid value"):
        ser[1] += 0.5

    with pytest.raises(TypeError, match="Invalid value"):
        ser.loc[1] += 0.5

    with pytest.raises(TypeError, match="Invalid value"):
        ser.iloc[1] += 0.5

    with pytest.raises(TypeError, match="Invalid value"):
        ser.iat[1] += 0.5

    with pytest.raises(TypeError, match="Invalid value"):
        ser.at[1] += 0.5

