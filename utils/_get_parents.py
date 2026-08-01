
def _get_parents(
    node: nodes.ClassDef, ignored_parents: frozenset[str]
) -> set[nodes.ClassDef]:
    return set(_get_parents_iter(node, ignored_parents))

