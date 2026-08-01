
def test_to_datetime_mixed_awareness_mixed_types(aware_val, naive_val, naive_first):
    # GH#55793, GH#55693, GH#57275
    # Empty string parses to NaT
    vals = [aware_val, naive_val, ""]

    vec = vals
    if naive_first:
        # alas, the behavior is order-dependent, so we test both ways
        vec = [naive_val, aware_val, ""]

    # both_strs-> paths that were previously already deprecated with warning
    #  issued in _array_to_datetime_object
    both_strs = isinstance(aware_val, str) and isinstance(naive_val, str)
    has_numeric = isinstance(naive_val, (int, float))
    both_datetime = isinstance(naive_val, datetime) and isinstance(aware_val, datetime)

    mixed_msg = (
        "Mixed timezones detected. Pass utc=True in to_datetime or tz='UTC' "
        "in DatetimeIndex to convert to a common timezone"
    )

    first_non_null = next(x for x in vec if x != "")
    # if first_non_null is a not a string, _guess_datetime_format_for_array
    #  doesn't guess a format so we don't go through array_strptime
    if not isinstance(first_non_null, str):
        # that case goes through array_strptime which has different behavior
        msg = mixed_msg
        if naive_first and isinstance(aware_val, Timestamp):
            if isinstance(naive_val, Timestamp):
                msg = "Tz-aware datetime.datetime cannot be converted to datetime64"
            with pytest.raises(ValueError, match=msg):
                to_datetime(vec)
        else:
            if not naive_first and both_datetime:
                msg = "Cannot mix tz-aware with tz-naive values"
            with pytest.raises(ValueError, match=msg):
                to_datetime(vec)

        # No warning/error with utc=True
        to_datetime(vec, utc=True)

    elif has_numeric and vec.index(aware_val) < vec.index(naive_val):
        msg = "time data .* doesn't match format"
        with pytest.raises(ValueError, match=msg):
            to_datetime(vec)
        with pytest.raises(ValueError, match=msg):
            to_datetime(vec, utc=True)

    elif both_strs and vec.index(aware_val) < vec.index(naive_val):
        msg = r"time data \"2020-01-01 00:00\" doesn't match format"
        with pytest.raises(ValueError, match=msg):
            to_datetime(vec)
        with pytest.raises(ValueError, match=msg):
            to_datetime(vec, utc=True)

    elif both_strs and vec.index(naive_val) < vec.index(aware_val):
        msg = "unconverted data remains when parsing with format"
        with pytest.raises(ValueError, match=msg):
            to_datetime(vec)
        with pytest.raises(ValueError, match=msg):
            to_datetime(vec, utc=True)

    else:
        msg = mixed_msg
        with pytest.raises(ValueError, match=msg):
            to_datetime(vec)

        # No warning/error with utc=True
        to_datetime(vec, utc=True)

    if both_strs:
        msg = mixed_msg
        with pytest.raises(ValueError, match=msg):
            to_datetime(vec, format="mixed")
        with pytest.raises(ValueError, match=msg):
            DatetimeIndex(vec)
    else:
        msg = mixed_msg
        if naive_first and isinstance(aware_val, Timestamp):
            if isinstance(naive_val, Timestamp):
                msg = "Tz-aware datetime.datetime cannot be converted to datetime64"
            with pytest.raises(ValueError, match=msg):
                to_datetime(vec, format="mixed")
            with pytest.raises(ValueError, match=msg):
                DatetimeIndex(vec)
        else:
            if not naive_first and both_datetime:
                msg = "Cannot mix tz-aware with tz-naive values"
            with pytest.raises(ValueError, match=msg):
                to_datetime(vec, format="mixed")
            with pytest.raises(ValueError, match=msg):
                DatetimeIndex(vec)

