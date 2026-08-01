
def test_where_period_invalid_na(frame_or_series, as_cat, request):
    # GH#44697
    idx = pd.period_range("2016-01-01", periods=3, freq="D")
    if as_cat:
        idx = idx.astype("category")
    obj = frame_or_series(idx)

    # NA value that we should *not* cast to Period dtype
    tdnat = pd.NaT.to_numpy("m8[ns]")

    mask = np.array([True, True, False], ndmin=obj.ndim).T

    if as_cat:
        msg = (
            r"Cannot setitem on a Categorical with a new category \(NaT\), "
            "set the categories first"
        )
    else:
        msg = "value should be a 'Period'"

    if as_cat:
        with pytest.raises(TypeError, match=msg):
            obj.where(mask, tdnat)

        with pytest.raises(TypeError, match=msg):
            obj.mask(mask, tdnat)

        with pytest.raises(TypeError, match=msg):
            obj.mask(mask, tdnat, inplace=True)

    else:
        # With PeriodDtype, ser[i] = tdnat coerces instead of raising,
        #  so for consistency, ser[mask] = tdnat must as well
        expected = obj.astype(object).where(mask, tdnat)
        result = obj.where(mask, tdnat)
        tm.assert_equal(result, expected)

        expected = obj.astype(object).mask(mask, tdnat)
        result = obj.mask(mask, tdnat)
        tm.assert_equal(result, expected)

        with pytest.raises(TypeError, match="Invalid value"):
            obj.mask(mask, tdnat, inplace=True)

