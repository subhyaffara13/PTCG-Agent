
def test_to_html_render_links(render_links, expected, datapath):
    # GH 2679
    data = [
        [0, "https://pandas.pydata.org/?q1=a&q2=b", "pydata.org"],
        [0, "www.pydata.org", "pydata.org"],
    ]
    df = DataFrame(data, columns=Index(["foo", "bar", None], dtype=object))

    result = df.to_html(render_links=render_links)
    expected = expected_html(datapath, expected)
    assert result == expected

