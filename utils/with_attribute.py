
def with_attribute(*args: tuple[str, str], **attr_dict) -> ParseAction:
    """
    Helper to create a validating parse action to be used with start
    tags created with :class:`make_xml_tags` or
    :class:`make_html_tags`. Use ``with_attribute`` to qualify
    a starting tag with a required attribute value, to avoid false
    matches on common tags such as ``<TD>`` or ``<DIV>``.

    Call ``with_attribute`` with a series of attribute names and
    values. Specify the list of filter attributes names and values as:

    - keyword arguments, as in ``(align="right")``, or
    - as an explicit dict with ``**`` operator, when an attribute
      name is also a Python reserved word, as in ``**{"class":"Customer", "align":"right"}``
    - a list of name-value tuples, as in ``(("ns1:class", "Customer"), ("ns2:align", "right"))``

    For attribute names with a namespace prefix, you must use the second
    form.  Attribute names are matched insensitive to upper/lower case.

    If just testing for ``class`` (with or without a namespace), use
    :class:`with_class`.

    To verify that the attribute exists, but without specifying a value,
    pass ``with_attribute.ANY_VALUE`` as the value.

    The next two examples use the following input data and tag parsers:

    .. testcode::

       html = '''
           <div>
           Some text
           <div type="grid">1 4 0 1 0</div>
           <div type="graph">1,3 2,3 1,1</div>
           <div>this has no type</div>
           </div>
       '''
       div,div_end = make_html_tags("div")

    Only match div tag having a type attribute with value "grid":

    .. testcode::

       div_grid = div().set_parse_action(with_attribute(type="grid"))
       grid_expr = div_grid + SkipTo(div | div_end)("body")
       for grid_header in grid_expr.search_string(html):
           print(grid_header.body)

    prints:

    .. testoutput::

       1 4 0 1 0

    Construct a match with any div tag having a type attribute,
    regardless of the value:

    .. testcode::

       div_any_type = div().set_parse_action(
           with_attribute(type=with_attribute.ANY_VALUE)
       )
       div_expr = div_any_type + SkipTo(div | div_end)("body")
       for div_header in div_expr.search_string(html):
           print(div_header.body)

    prints:

    .. testoutput::

       1 4 0 1 0
       1,3 2,3 1,1
    """
    attrs_list: list[tuple[str, str]] = []
    if args:
        attrs_list.extend(args)
    else:
        attrs_list.extend(attr_dict.items())

    def pa(s: str, l: int, tokens: ParseResults) -> None:
        for attrName, attrValue in attrs_list:
            if attrName not in tokens:
                raise ParseException(s, l, f"no matching attribute {attrName!r}")
            if attrValue != with_attribute.ANY_VALUE and tokens[attrName] != attrValue:  # type: ignore [attr-defined]
                raise ParseException(
                    s,
                    l,
                    f"attribute {attrName!r} has value {tokens[attrName]!r}, must be {attrValue!r}",
                )

    return pa


def withAttribute(*args, **attrDict):
    """Helper to create a validating parse action to be used with start
    tags created with :class:`makeXMLTags` or
    :class:`makeHTMLTags`. Use ``withAttribute`` to qualify
    a starting tag with a required attribute value, to avoid false
    matches on common tags such as ``<TD>`` or ``<DIV>``.

    Call ``withAttribute`` with a series of attribute names and
    values. Specify the list of filter attributes names and values as:

     - keyword arguments, as in ``(align="right")``, or
     - as an explicit dict with ``**`` operator, when an attribute
       name is also a Python reserved word, as in ``**{"class":"Customer", "align":"right"}``
     - a list of name-value tuples, as in ``(("ns1:class", "Customer"), ("ns2:align", "right"))``

    For attribute names with a namespace prefix, you must use the second
    form.  Attribute names are matched insensitive to upper/lower case.

    If just testing for ``class`` (with or without a namespace), use
    :class:`withClass`.

    To verify that the attribute exists, but without specifying a value,
    pass ``withAttribute.ANY_VALUE`` as the value.

    Example::

        html = '''
            <div>
            Some text
            <div type="grid">1 4 0 1 0</div>
            <div type="graph">1,3 2,3 1,1</div>
            <div>this has no type</div>
            </div>

        '''
        div,div_end = makeHTMLTags("div")

        # only match div tag having a type attribute with value "grid"
        div_grid = div().setParseAction(withAttribute(type="grid"))
        grid_expr = div_grid + SkipTo(div | div_end)("body")
        for grid_header in grid_expr.searchString(html):
            print(grid_header.body)

        # construct a match with any div tag having a type attribute, regardless of the value
        div_any_type = div().setParseAction(withAttribute(type=withAttribute.ANY_VALUE))
        div_expr = div_any_type + SkipTo(div | div_end)("body")
        for div_header in div_expr.searchString(html):
            print(div_header.body)

    prints::

        1 4 0 1 0

        1 4 0 1 0
        1,3 2,3 1,1
    """
    if args:
        attrs = args[:]
    else:
        attrs = attrDict.items()
    attrs = [(k, v) for k, v in attrs]
    def pa(s, l, tokens):
        for attrName, attrValue in attrs:
            if attrName not in tokens:
                raise ParseException(s, l, "no matching attribute " + attrName)
            if attrValue != withAttribute.ANY_VALUE and tokens[attrName] != attrValue:
                raise ParseException(s, l, "attribute '%s' has value '%s', must be '%s'" %
                                            (attrName, tokens[attrName], attrValue))
    return pa

