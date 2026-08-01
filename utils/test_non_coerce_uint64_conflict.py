
def test_non_coerce_uint64_conflict():
    # see gh-17007 and gh-17125
    #
    # For completeness.
    ser = Series(["12345678901234567890", "1234567890", "ITEM"])

    with pytest.raises(ValueError, match="Unable to parse string"):
        to_numeric(ser, errors="raise")

