
def test_parse_multiple_delimited_dates_with_swap_warnings():
    # GH46210
    with pytest.raises(
        ValueError,
        match=(
            r'^time data "31/05/2000" doesn\'t match format "%m/%d/%Y". '
            r"You might want to try:"
        ),
    ):
        pd.to_datetime(["01/01/2000", "31/05/2000", "31/05/2001", "01/02/2000"])

