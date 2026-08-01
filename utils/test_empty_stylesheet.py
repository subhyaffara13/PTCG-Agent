
def test_empty_stylesheet(val, kml_cta_rail_lines):
    lxml_etree = pytest.importorskip("lxml.etree")
    with pytest.raises(lxml_etree.XMLSyntaxError):
        read_xml(kml_cta_rail_lines, stylesheet=val)

