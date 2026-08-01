
def test_url_urlopen(httpserver):
    data = """\
A         B            C            D
201158    360.242940   149.910199   11950.7
201159    444.953632   166.985655   11788.4
201160    364.136849   183.628767   11806.2
201161    413.836124   184.375703   11916.8
201162    502.953953   173.237159   12468.3
"""
    httpserver.serve_content(content=data)
    expected = pd.Index(list("ABCD"))
    with urlopen(httpserver.url) as f:
        result = read_fwf(f).columns

    tm.assert_index_equal(result, expected)

