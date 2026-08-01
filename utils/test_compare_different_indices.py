
def test_compare_different_indices():
    msg = "Can only compare identically-labeled Series objects"
    ser1 = pd.Series([1, 2, 3], index=["a", "b", "c"])
    ser2 = pd.Series([1, 2, 3], index=["a", "b", "d"])
    with pytest.raises(ValueError, match=msg):
        ser1.compare(ser2)


def test_compare_different_indices():
    msg = (
        r"Can only compare identically-labeled \(both index and columns\) DataFrame "
        "objects"
    )
    df1 = pd.DataFrame([1, 2, 3], index=["a", "b", "c"])
    df2 = pd.DataFrame([1, 2, 3], index=["a", "b", "d"])
    with pytest.raises(ValueError, match=msg):
        df1.compare(df2)

