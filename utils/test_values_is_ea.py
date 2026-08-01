
def test_values_is_ea():
    df = DataFrame({"a": date_range("2012-01-01", periods=3)})
    arr = np.asarray(df)
    assert arr.flags.writeable is False

