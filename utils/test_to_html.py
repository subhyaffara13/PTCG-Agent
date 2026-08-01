
def test_to_html(biggie_df_fixture):
    # TODO: split this test
    df = biggie_df_fixture
    s = df.to_html()

    buf = StringIO()
    retval = df.to_html(buf=buf)
    assert retval is None
    assert buf.getvalue() == s

    assert isinstance(s, str)

    df.to_html(columns=["B", "A"], col_space=17)
    df.to_html(columns=["B", "A"], formatters={"A": lambda x: f"{x:.1f}"})

    df.to_html(columns=["B", "A"], float_format=str)
    df.to_html(columns=["B", "A"], col_space=12, float_format=str)

