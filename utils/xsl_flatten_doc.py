
def xsl_flatten_doc(xml_data_path, datapath):
    """
    Returns the path (as `str`) to the `flatten_doc.xsl` example file.

    Examples
    --------
    >>> def test_read_xsl(xsl_flatten_doc, mode):
    ...     with open(
    ...         xsl_flatten_doc, mode, encoding="utf-8" if mode == "r" else None
    ...     ) as f:
    ...         xsl_obj = f.read()
    """
    return datapath(xml_data_path / "flatten_doc.xsl")

