
def test_where_nullable_invalid_na(frame_or_series, any_numeric_ea_dtype):
    # GH#44697
    arr = pd.array([1, 2, 3], dtype=any_numeric_ea_dtype)
    obj = frame_or_series(arr)

    mask = np.array([True, True, False], ndmin=obj.ndim).T

    msg = r"Invalid value '.*' for dtype '(U?Int|Float)\d{1,2}'"

    for null in [*tm.NP_NAT_OBJECTS, pd.NaT]:
        # NaT is an NA value that we should *not* cast to pd.NA dtype
        with pytest.raises(TypeError, match=msg):
            obj.where(mask, null)

        with pytest.raises(TypeError, match=msg):
            obj.mask(mask, null)

