
def test_to_html_filename(biggie_df_fixture, tmpdir):
    df = biggie_df_fixture
    expected = df.to_html()
    path = tmpdir.join("test.html")
    df.to_html(path)
    result = path.read()
    assert result == expected

