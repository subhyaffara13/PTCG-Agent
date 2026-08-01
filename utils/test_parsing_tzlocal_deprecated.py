
def test_parsing_tzlocal_deprecated():
    # GH#50791
    msg = "|".join(
        [
            r"Parsing 'EST' as tzlocal \(dependent on system timezone\) "
            r"is no longer supported\. "
            "Pass the 'tz' keyword or call tz_localize after construction instead",
            ".*included an un-recognized timezone",
        ]
    )
    dtstr = "Jan 15 2004 03:00 EST"

    with tm.set_timezone("US/Eastern"):
        with pytest.raises(ValueError, match=msg):
            parse_datetime_string_with_reso(dtstr)

        with pytest.raises(ValueError, match=msg):
            parsing.py_parse_datetime_string(dtstr)

        with pytest.raises(ValueError, match=msg):
            Timestamp(dtstr)

