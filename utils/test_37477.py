
def test_37477():
    # fixed by GH#45121
    orig = DataFrame({"A": [1, 2, 3], "B": [3, 4, 5]})

    df = orig.copy()
    with pytest.raises(TypeError, match="Invalid value"):
        df.at[1, "B"] = 1.2

    with pytest.raises(TypeError, match="Invalid value"):
        df.loc[1, "B"] = 1.2

    with pytest.raises(TypeError, match="Invalid value"):
        df.iat[1, 1] = 1.2

    with pytest.raises(TypeError, match="Invalid value"):
        df.iloc[1, 1] = 1.2

