
def xsl_row_field_output(xml_data_path, datapath):
    """
    Returns the path (as `str`) to the `row_field_output.xsl` example file.

    Examples
    --------
    >>> def test_read_xsl(xsl_row_field_output, mode):
    ...     with open(
    ...         xsl_row_field_output, mode, encoding="utf-8" if mode == "r" else None
    ...     ) as f:
    ...         xsl_obj = f.read()
    """
    return datapath(xml_data_path / "row_field_output.xsl")

