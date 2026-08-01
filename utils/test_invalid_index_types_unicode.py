
def test_invalid_index_types_unicode():
    # see gh-10822
    #
    # Odd error message on conversions to datetime for unicode.
    msg = "Unknown datetime string format"

    with pytest.raises(ValueError, match=msg):
        frequencies.infer_freq(Index(["ZqgszYBfuL"]))

