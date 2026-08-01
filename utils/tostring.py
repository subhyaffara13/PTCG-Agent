
def tostring(row):
    """Convert row of bytes to string.  Expects `row` to be an
    ``array``.
    """
    return row.tobytes()


def tostring(element):
    """Serialize an element and its child nodes to a string"""
    rv = []

    def serializeElement(element):
        if not hasattr(element, "tag"):
            if element.docinfo.internalDTD:
                if element.docinfo.doctype:
                    dtd_str = element.docinfo.doctype
                else:
                    dtd_str = "<!DOCTYPE %s>" % element.docinfo.root_name
                rv.append(dtd_str)
            serializeElement(element.getroot())

        elif element.tag == comment_type:
            rv.append("<!--%s-->" % (element.text,))

        else:
            # This is assumed to be an ordinary element
            if not element.attrib:
                rv.append("<%s>" % (element.tag,))
            else:
                attr = " ".join(["%s=\"%s\"" % (name, value)
                                 for name, value in element.attrib.items()])
                rv.append("<%s %s>" % (element.tag, attr))
            if element.text:
                rv.append(element.text)

            for child in element:
                serializeElement(child)

            rv.append("</%s>" % (element.tag,))

        if hasattr(element, "tail") and element.tail:
            rv.append(element.tail)

    serializeElement(element)

    return "".join(rv)

