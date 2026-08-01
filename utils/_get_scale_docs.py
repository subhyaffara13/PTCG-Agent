
def _get_scale_docs():
    """
    Helper function for generating docstrings related to scales.
    """
    docs = []
    for name, scale_class in _scale_mapping.items():
        docstring = inspect.getdoc(scale_class.__init__) or ""
        docs.extend([
            f"    {name!r}",
            "",
            textwrap.indent(docstring, " " * 8),
            ""
        ])
    return "\n".join(docs)

