
def test_to_datetime_lxml_elementunicoderesult_with_format(cache):
    etree = pytest.importorskip("lxml.etree")

    s = "2025-02-05 16:59:57"
    node = etree.XML(f"<date>{s}</date>")
    val = node.xpath("/date/node()")[0]  # _ElementUnicodeResult

    out = to_datetime(Series([val]), format="%Y-%m-%d %H:%M:%S", cache=cache)
    assert out.iloc[0] == Timestamp(s)

