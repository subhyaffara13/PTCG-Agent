
def _glifTreeFromString(aString: Union[str, bytes]) -> ElementType:
    data = tobytes(aString, encoding="utf-8")
    try:
        if etree._have_lxml:
            root = etree.fromstring(data, parser=etree.XMLParser(remove_comments=True))
        else:
            root = etree.fromstring(data)
    except Exception as etree_exception:
        raise GlifLibError("GLIF contains invalid XML.") from etree_exception

    if root.tag != "glyph":
        raise GlifLibError("The GLIF is not properly formatted.")
    if root.text and root.text.strip() != "":
        raise GlifLibError("Invalid GLIF structure.")
    return root

