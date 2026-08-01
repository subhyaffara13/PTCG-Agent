
def _finder_template(
    name: str, mapping: Mapping[str, str], namespaces: dict[str, list[str]]
) -> str:
    """Create a string containing the code for the``MetaPathFinder`` and
    ``PathEntryFinder``.
    """
    mapping = dict(sorted(mapping.items(), key=operator.itemgetter(0)))
    return _FINDER_TEMPLATE.format(name=name, mapping=mapping, namespaces=namespaces)

