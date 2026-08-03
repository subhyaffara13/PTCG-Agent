from pathlib import Path


def xml_data_path():
    """
    Returns a Path object to the XML example directory.

    Examples
    --------
    >>> def test_read_xml(xml_data_path):
    ...     pd.read_xml(xml_data_path / "file.xsl")
    """
    return Path(__file__).parent.parent / "data" / "xml"

