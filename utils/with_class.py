
def with_class(classname: str, namespace: str = "") -> ParseAction:
    """
    Simplified version of :meth:`with_attribute` when
    matching on a div class - made difficult because ``class`` is
    a reserved word in Python.

    Using similar input data to the :meth:`with_attribute` examples:

    .. testcode::

       html = '''
           <div>
           Some text
           <div class="grid">1 4 0 1 0</div>
           <div class="graph">1,3 2,3 1,1</div>
           <div>this &lt;div&gt; has no class</div>
           </div>
       '''
       div,div_end = make_html_tags("div")

    Only match div tag having the "grid" class:

    .. testcode::

       div_grid = div().set_parse_action(with_class("grid"))
       grid_expr = div_grid + SkipTo(div | div_end)("body")
       for grid_header in grid_expr.search_string(html):
           print(grid_header.body)

    prints:

    .. testoutput::

       1 4 0 1 0

    Construct a match with any div tag having a class attribute,
    regardless of the value:

    .. testcode::

       div_any_type = div().set_parse_action(
           with_class(withAttribute.ANY_VALUE)
       )
       div_expr = div_any_type + SkipTo(div | div_end)("body")
       for div_header in div_expr.search_string(html):
           print(div_header.body)

    prints:

    .. testoutput::

       1 4 0 1 0
       1,3 2,3 1,1
    """
    classattr = f"{namespace}:class" if namespace else "class"
    return with_attribute(**{classattr: classname})


def withClass(classname, namespace=''):
    """Simplified version of :class:`withAttribute` when
    matching on a div class - made difficult because ``class`` is
    a reserved word in Python.

    Example::

        html = '''
            <div>
            Some text
            <div class="grid">1 4 0 1 0</div>
            <div class="graph">1,3 2,3 1,1</div>
            <div>this &lt;div&gt; has no class</div>
            </div>

        '''
        div,div_end = makeHTMLTags("div")
        div_grid = div().setParseAction(withClass("grid"))

        grid_expr = div_grid + SkipTo(div | div_end)("body")
        for grid_header in grid_expr.searchString(html):
            print(grid_header.body)

        div_any_type = div().setParseAction(withClass(withAttribute.ANY_VALUE))
        div_expr = div_any_type + SkipTo(div | div_end)("body")
        for div_header in div_expr.searchString(html):
            print(div_header.body)

    prints::

        1 4 0 1 0

        1 4 0 1 0
        1,3 2,3 1,1
    """
    classattr = "%s:class" % namespace if namespace else "class"
    return withAttribute(**{classattr: classname})

