
def test_outer():
    # https://github.com/pandas-dev/pandas/issues/27186
    ser = pd.Series([1, 2, 3])
    obj = np.array([1, 2, 3])

    with pytest.raises(NotImplementedError, match="^$"):
        np.subtract.outer(ser, obj)

