
def xml_doc_ch_utf(xml_data_path, datapath):
    """
    Returns the path (as `str`) to the `doc_ch_utf.xml` example file.

    Examples
    --------
    >>> def test_read_xml(xml_doc_ch_utf):
    ...     pd.read_xml(xml_doc_ch_utf)
    """
    return datapath(xml_data_path / "doc_ch_utf.xml")

