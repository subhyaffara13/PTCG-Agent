
def kml_cta_rail_lines(xml_data_path, datapath):
    """
    Returns the path (as `str`) to the `cta_rail_lines.kml` example file.

    Examples
    --------
    >>> def test_read_xml(kml_cta_rail_lines):
    ...     pd.read_xml(
    ...         kml_cta_rail_lines,
    ...         xpath=".//k:Placemark",
    ...         namespaces={"k": "http://www.opengis.net/kml/2.2"},
    ...         stylesheet=xsl_flatten_doc,
    ...     )
    """
    return datapath(xml_data_path / "cta_rail_lines.kml")

