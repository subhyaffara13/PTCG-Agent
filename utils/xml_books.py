
def xml_books(xml_data_path, datapath):
    """
    Returns the path (as `str`) to the `books.xml` example file.

    Examples
    --------
    >>> def test_read_xml(xml_books):
    ...     pd.read_xml(xml_books)
    """
    return datapath(xml_data_path / "books.xml")

