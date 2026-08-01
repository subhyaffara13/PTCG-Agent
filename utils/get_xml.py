
def getXML(func, ttFont=None):
    """Call the passed toXML function and return the written content as a
    list of lines (unicode strings).
    Result is stripped of XML declaration and OS-specific newline characters.
    """
    writer = makeXMLWriter()
    func(writer, ttFont)
    xml = writer.file.getvalue().decode("utf-8")
    # toXML methods must always end with a writer.newline()
    assert xml.endswith("\n")
    return xml.splitlines()

