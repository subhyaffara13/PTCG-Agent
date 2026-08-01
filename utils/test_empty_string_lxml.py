
def test_empty_string_lxml(val):
    lxml_etree = pytest.importorskip("lxml.etree")

    msg = "|".join(
        [
            "Document is empty",
            # Seen on Mac with lxml 4.91
            r"None \(line 0\)",
        ]
    )
    if isinstance(val, str):
        data = StringIO(val)
    else:
        data = BytesIO(val)
    with pytest.raises(lxml_etree.XMLSyntaxError, match=msg):
        read_xml(data, parser="lxml")

