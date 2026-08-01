
def test_empty_string_stylesheet(val, geom_df):
    lxml_etree = pytest.importorskip("lxml.etree")

    msg = "|".join(
        [
            "Document is empty",
            "Start tag expected, '<' not found",
            # Seen on Mac with lxml 4.9.1
            r"None \(line 0\)",
        ]
    )

    with pytest.raises(lxml_etree.XMLSyntaxError, match=msg):
        geom_df.to_xml(stylesheet=val)

