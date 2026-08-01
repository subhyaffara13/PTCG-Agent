
def test_url(httpserver, xml_file):
    pytest.importorskip("lxml")
    with open(xml_file, encoding="utf-8") as f:
        httpserver.serve_content(content=f.read())
        df_url = read_xml(httpserver.url, xpath=".//book[count(*)=4]")

    df_expected = DataFrame(
        {
            "category": ["cooking", "children", "web"],
            "title": ["Everyday Italian", "Harry Potter", "Learning XML"],
            "author": ["Giada De Laurentiis", "J K. Rowling", "Erik T. Ray"],
            "year": [2005, 2005, 2003],
            "price": [30.00, 29.99, 39.95],
        }
    )

    tm.assert_frame_equal(df_url, df_expected)


def test_url(all_parsers, csv_dir_path, httpserver):
    parser = all_parsers
    kwargs = {"sep": "\t"}

    local_path = os.path.join(csv_dir_path, "salaries.csv")
    with open(local_path, encoding="utf-8") as f:
        httpserver.serve_content(content=f.read())

    url_result = parser.read_csv(httpserver.url, **kwargs)

    local_result = parser.read_csv(local_path, **kwargs)
    tm.assert_frame_equal(url_result, local_result)


def test_url():
    # Test that object url appears in output svg.

    fig, ax = plt.subplots()

    # collections
    s = ax.scatter([1, 2, 3], [4, 5, 6])
    s.set_urls(['https://example.com/foo', 'https://example.com/bar', None])

    # Line2D
    p, = plt.plot([2, 3, 4], [4, 5, 6])
    p.set_url('https://example.com/baz')

    # Line2D markers-only
    p, = plt.plot([3, 4, 5], [4, 5, 6], linestyle='none', marker='x')
    p.set_url('https://example.com/quux')

    b = BytesIO()
    fig.savefig(b, format='svg')
    b = b.getvalue()
    for v in [b'foo', b'bar', b'baz', b'quux']:
        assert b'https://example.com/' + v in b

