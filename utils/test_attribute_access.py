
def test_attribute_access(test_frame):
    r = test_frame.resample("h")
    tm.assert_series_equal(r.A.sum(), r["A"].sum())


def test_attribute_access():
    df = DataFrame([[1, 2]], columns=["A", "B"])
    r = df.rolling(window=5)
    tm.assert_series_equal(r.A.sum(), r["A"].sum())
    msg = "'Rolling' object has no attribute 'F'"
    with pytest.raises(AttributeError, match=msg):
        r.F

