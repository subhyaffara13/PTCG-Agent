
def document_properties(mark):

    properties = [f.name for f in fields(mark) if isinstance(f.default, Mappable)]
    text = [
        "",
        "    This mark defines the following properties:",
        textwrap.fill(
            ", ".join([f"|{p}|" for p in properties]),
            width=78, initial_indent=" " * 8, subsequent_indent=" " * 8,
        ),
    ]

    docstring_lines = mark.__doc__.split("\n")
    new_docstring = "\n".join([
        *docstring_lines[:2],
        *text,
        *docstring_lines[2:],
    ])
    mark.__doc__ = new_docstring
    return mark

