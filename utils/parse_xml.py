
def parseXML(xmlSnippet):
    """Parses a snippet of XML.

    Input can be either a single string (unicode or UTF-8 bytes), or a
    a sequence of strings.

    The result is in the same format that would be returned by
    XMLReader, but the parser imposes no constraints on the root
    element so it can be called on small snippets of TTX files.
    """
    # To support snippets with multiple elements, we add a fake root.
    reader = TestXMLReader_()
    xml = b"<root>"
    if isinstance(xmlSnippet, bytes):
        xml += xmlSnippet
    elif isinstance(xmlSnippet, str):
        xml += tobytes(xmlSnippet, "utf-8")
    elif isinstance(xmlSnippet, Iterable):
        xml += b"".join(tobytes(s, "utf-8") for s in xmlSnippet)
    else:
        raise TypeError(
            "expected string or sequence of strings; found %r"
            % type(xmlSnippet).__name__
        )
    xml += b"</root>"
    reader.parser.Parse(xml, 1)
    return reader.root[2]

