
def docstringify(
    docstring: nodes.Const | None, default_type: str = "default"
) -> Docstring:
    best_match = (0, DOCSTRING_TYPES.get(default_type, Docstring)(docstring))
    for docstring_type in (
        SphinxDocstring,
        EpytextDocstring,
        GoogleDocstring,
        NumpyDocstring,
    ):
        instance = docstring_type(docstring)
        matching_sections = instance.matching_sections()
        if matching_sections > best_match[0]:
            best_match = (matching_sections, instance)

    return best_match[1]

