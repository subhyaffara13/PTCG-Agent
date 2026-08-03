import sys

def testSerializer(element):
    rv = []
    infosetFilter = _ihatexml.InfosetFilter(preventDoubleDashComments=True)

    def serializeElement(element, indent=0):
        if not hasattr(element, "tag"):
            if hasattr(element, "getroot"):
                # Full tree case
                rv.append("#document")
                if element.docinfo.internalDTD:
                    if not (element.docinfo.public_id or
                            element.docinfo.system_url):
                        dtd_str = "<!DOCTYPE %s>" % element.docinfo.root_name
                    else:
                        dtd_str = """<!DOCTYPE %s "%s" "%s">""" % (
                            element.docinfo.root_name,
                            element.docinfo.public_id,
                            element.docinfo.system_url)
                    rv.append("|%s%s" % (' ' * (indent + 2), dtd_str))
                next_element = element.getroot()
                while next_element.getprevious() is not None:
                    next_element = next_element.getprevious()
                while next_element is not None:
                    serializeElement(next_element, indent + 2)
                    next_element = next_element.getnext()
            elif isinstance(element, str) or isinstance(element, bytes):
                # Text in a fragment
                assert isinstance(element, str) or sys.version_info[0] == 2
                rv.append("|%s\"%s\"" % (' ' * indent, element))
            else:
                # Fragment case
                rv.append("#document-fragment")
                for next_element in element:
                    serializeElement(next_element, indent + 2)
        elif element.tag == comment_type:
            rv.append("|%s<!-- %s -->" % (' ' * indent, element.text))
            if hasattr(element, "tail") and element.tail:
                rv.append("|%s\"%s\"" % (' ' * indent, element.tail))
        else:
            assert isinstance(element, etree._Element)
            nsmatch = etree_builders.tag_regexp.match(element.tag)
            if nsmatch is not None:
                ns = nsmatch.group(1)
                tag = nsmatch.group(2)
                prefix = constants.prefixes[ns]
                rv.append("|%s<%s %s>" % (' ' * indent, prefix,
                                          infosetFilter.fromXmlName(tag)))
            else:
                rv.append("|%s<%s>" % (' ' * indent,
                                       infosetFilter.fromXmlName(element.tag)))

            if hasattr(element, "attrib"):
                attributes = []
                for name, value in element.attrib.items():
                    nsmatch = tag_regexp.match(name)
                    if nsmatch is not None:
                        ns, name = nsmatch.groups()
                        name = infosetFilter.fromXmlName(name)
                        prefix = constants.prefixes[ns]
                        attr_string = "%s %s" % (prefix, name)
                    else:
                        attr_string = infosetFilter.fromXmlName(name)
                    attributes.append((attr_string, value))

                for name, value in sorted(attributes):
                    rv.append('|%s%s="%s"' % (' ' * (indent + 2), name, value))

            if element.text:
                rv.append("|%s\"%s\"" % (' ' * (indent + 2), element.text))
            indent += 2
            for child in element:
                serializeElement(child, indent)
            if hasattr(element, "tail") and element.tail:
                rv.append("|%s\"%s\"" % (' ' * (indent - 2), element.tail))
    serializeElement(element, 0)

    return "\n".join(rv)

