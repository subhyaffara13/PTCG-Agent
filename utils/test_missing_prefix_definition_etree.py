
def test_missing_prefix_definition_etree(kml_cta_rail_lines):
    with pytest.raises(SyntaxError, match=("you used an undeclared namespace prefix")):
        read_xml(kml_cta_rail_lines, xpath=".//kml:Placemark", parser="etree")

