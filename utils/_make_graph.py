
def _make_graph(
    filename: str, dep_info: dict[str, set[str]], sect: Section, gtype: str
) -> None:
    """Generate a dependencies graph and add some information about it in the
    report's section.
    """
    outputfile = _dependencies_graph(filename, dep_info)
    sect.append(Paragraph((f"{gtype}imports graph has been written to {outputfile}",)))

