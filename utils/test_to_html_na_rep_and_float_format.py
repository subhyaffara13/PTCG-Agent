
def test_to_html_na_rep_and_float_format(na_rep, datapath):
    # https://github.com/pandas-dev/pandas/issues/13828
    df = DataFrame(
        [
            ["A", 1.2225],
            ["A", None],
        ],
        columns=["Group", "Data"],
    )
    result = df.to_html(na_rep=na_rep, float_format="{:.2f}".format)
    expected = expected_html(datapath, "gh13828_expected_output")
    expected = expected.format(na_rep=na_rep)
    assert result == expected

