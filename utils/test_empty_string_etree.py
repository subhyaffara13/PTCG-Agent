
def test_empty_string_etree(val):
    if isinstance(val, str):
        data = StringIO(val)
    else:
        data = BytesIO(val)
    with pytest.raises(ParseError, match="no element found"):
        read_xml(data, parser="etree")

