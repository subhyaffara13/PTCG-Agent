
def test_keyword_deprecation():
    # GH 57280
    msg = (
        "Starting with pandas version 4.0 all arguments of to_markdown "
        "except for the argument 'buf' will be keyword-only."
    )
    s = pd.Series()
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        s.to_markdown(None, "wt")

