
def test_datetime_timedelta_cast(dtype, input_data, input_dtype):

    a = np.array(input_data, dtype=input_dtype)

    has_na = hasattr(dtype, "na_object")
    is_str = isinstance(getattr(dtype, "na_object", None), str)

    if not has_na or is_str:
        a = np.delete(a, 3)

    sa = a.astype(dtype)
    ra = sa.astype(a.dtype)

    if has_na and not is_str:
        assert sa[3] is dtype.na_object
        assert np.isnat(ra[3])

    assert_array_equal(a, ra)

    if has_na and not is_str:
        # don't worry about comparing how NaT is converted
        sa = np.delete(sa, 3)
        a = np.delete(a, 3)

    if input_dtype.startswith("M"):
        assert_array_equal(sa, a.astype("U"))
    else:
        # The timedelta to unicode cast produces strings
        # that aren't round-trippable and we don't want to
        # reproduce that behavior in stringdtype
        assert_array_equal(sa, a.astype("int64").astype("U"))

