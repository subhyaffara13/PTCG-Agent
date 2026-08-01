
def xml_baby_names(xml_data_path, datapath):
    """
    Returns the path (as `str`) to the `baby_names.xml` example file.

    Examples
    --------
    >>> def test_read_xml(xml_baby_names):
    ...     pd.read_xml(xml_baby_names)
    """
    return datapath(xml_data_path / "baby_names.xml")

