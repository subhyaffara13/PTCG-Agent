
def test_string_datetime_like_compat():
    # see gh-6463
    data = ["2004-01", "2004-02", "2004-03", "2004-04"]

    expected = frequencies.infer_freq(data)
    result = frequencies.infer_freq(Index(data))

    assert result == expected

