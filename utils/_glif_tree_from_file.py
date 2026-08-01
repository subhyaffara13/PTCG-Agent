
def _glifTreeFromFile(aFile: Union[str, bytes, int]) -> ElementType:
    if etree._have_lxml:
        tree = etree.parse(aFile, parser=etree.XMLParser(remove_comments=True))
    else:
        tree = etree.parse(aFile)
    root = tree.getroot()
    if root.tag != "glyph":
        raise GlifLibError("The GLIF is not properly formatted.")
    if root.text and root.text.strip() != "":
        raise GlifLibError("Invalid GLIF structure.")
    return root

