
def test_to_html_decimal(datapath):
    # GH 12031
    df = DataFrame({"A": [6.0, 3.1, 2.2]})
    result = df.to_html(decimal=",")
    expected = expected_html(datapath, "gh12031_expected_output")
    assert result == expected

