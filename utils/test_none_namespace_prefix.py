
def test_none_namespace_prefix(key):
    pytest.importorskip("lxml")
    with pytest.raises(
        TypeError, match=("empty namespace prefix is not supported in XPath")
    ):
        read_xml(
            StringIO(xml_default_nmsp),
            xpath=".//kml:Placemark",
            namespaces={key: "http://www.opengis.net/kml/2.2"},
            parser="lxml",
        )

