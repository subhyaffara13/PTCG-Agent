
def test_value_counts_object_inference_deprecated():
    # GH#56161
    dti = pd.date_range("2016-01-01", periods=3, tz="UTC")

    idx = dti.astype(object)
    res = idx.value_counts()

    exp = dti.value_counts()
    exp.index = exp.index.astype(object)
    tm.assert_series_equal(res, exp)

