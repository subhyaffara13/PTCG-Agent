
def make_xml_tags(
    tag_str: Union[str, ParserElement],
) -> tuple[ParserElement, ParserElement]:
    """Helper to construct opening and closing tag expressions for XML,
    given a tag name. Matches tags only in the given upper/lower case.

    Example: similar to :class:`make_html_tags`
    """
    return _makeTags(tag_str, True)


def makeXMLTags(tagStr):
    """Helper to construct opening and closing tag expressions for XML,
    given a tag name. Matches tags only in the given upper/lower case.

    Example: similar to :class:`makeHTMLTags`
    """
    return _makeTags(tagStr, True)

