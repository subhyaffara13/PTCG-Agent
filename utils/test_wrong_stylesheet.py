
def test_wrong_stylesheet(kml_cta_rail_lines, xml_data_path):
    pytest.importorskip("lxml.etree")

    xsl = xml_data_path / "flatten_doesnt_exist.xsl"

    with pytest.raises(
        FileNotFoundError, match=r"\[Errno 2\] No such file or directory"
    ):
        read_xml(kml_cta_rail_lines, stylesheet=xsl)

