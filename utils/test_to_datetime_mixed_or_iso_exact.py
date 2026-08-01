
def test_to_datetime_mixed_or_iso_exact(exact, format):
    msg = "Cannot use 'exact' when 'format' is 'mixed' or 'ISO8601'"
    with pytest.raises(ValueError, match=msg):
        to_datetime(["2020-01-01"], exact=exact, format=format)

