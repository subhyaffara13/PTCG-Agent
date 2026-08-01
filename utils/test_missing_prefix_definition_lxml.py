
def test_missing_prefix_definition_lxml(kml_cta_rail_lines):
    lxml_etree = pytest.importorskip("lxml.etree")

    with pytest.raises(lxml_etree.XPathEvalError, match=("Undefined namespace prefix")):
        read_xml(kml_cta_rail_lines, xpath=".//kml:Placemark", parser="lxml")

