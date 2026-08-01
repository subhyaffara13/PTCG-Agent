
def test_non_nano_value():
    # https://github.com/pandas-dev/pandas/issues/49076
    result = Timedelta(10, unit="D").as_unit("s").value
    # `.value` shows nanoseconds, even though unit is 's'
    assert result == 864000000000000

    # out-of-nanoseconds-bounds `.value` raises informative message
    msg = (
        r"Cannot convert Timedelta to nanoseconds without overflow. "
        r"Use `.asm8.view\('i8'\)` to cast represent Timedelta in its "
        r"own unit \(here, s\).$"
    )
    td = Timedelta(1_000, "D").as_unit("s") * 1_000
    with pytest.raises(OverflowError, match=msg):
        td.value
    # check that the suggested workaround actually works
    result = td.asm8.view("i8")
    assert result == 86400000000


def test_non_nano_value():
    # https://github.com/pandas-dev/pandas/issues/49076
    msg = "The 'unit' keyword is only used when"
    with tm.assert_produces_warning(UserWarning, match=msg):
        result = Timestamp("1800-01-01", unit="s").value
    # `.value` shows nanoseconds, even though unit is 's'
    assert result == -5364662400000000000

    # out-of-nanoseconds-bounds `.value` raises informative message
    msg = (
        r"Cannot convert Timestamp to nanoseconds without overflow. "
        r"Use `.asm8.view\('i8'\)` to cast represent Timestamp in its "
        r"own unit \(here, us\).$"
    )
    ts = Timestamp("0300-01-01")
    assert ts.unit == "us"
    with pytest.raises(OverflowError, match=msg):
        ts.value
    # check that the suggested workaround actually works
    result = ts.asm8.view("i8")
    assert result == -52_700_112_000 * 10**6

