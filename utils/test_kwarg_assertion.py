
def test_kwarg_assertion(kwargs):
    err_message = (
        "cannot construct a Timedelta from the passed arguments, "
        "allowed keywords are "
        "[weeks, days, hours, minutes, seconds, "
        "milliseconds, microseconds, nanoseconds]"
    )

    with pytest.raises(ValueError, match=re.escape(err_message)):
        Timedelta(**kwargs)

    with pytest.raises(ValueError, match=re.escape(err_message)):
        # GH#53801 'unit' misspelled as 'units'
        Timedelta(1, units="hours")

