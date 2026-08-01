
def _get_parents_iter(
    node: nodes.ClassDef, ignored_parents: frozenset[str]
) -> Iterator[nodes.ClassDef]:
    r"""Get parents of ``node``, excluding ancestors of ``ignored_parents``.

    If we have the following inheritance diagram:

             F
            /
        D  E
         \/
          B  C
           \/
            A      # class A(B, C): ...

    And ``ignored_parents`` is ``{"E"}``, then this function will return
    ``{A, B, C, D}`` -- both ``E`` and its ancestors are excluded.
    """
    parents: set[nodes.ClassDef] = set()
    to_explore = list(node.ancestors(recurs=False))
    while to_explore:
        parent = to_explore.pop()
        if parent.qname() in ignored_parents:
            continue
        if parent not in parents:
            # This guard might appear to be performing the same function as
            # adding the resolved parents to a set to eliminate duplicates
            # (legitimate due to diamond inheritance patterns), but its
            # additional purpose is to prevent cycles (not normally possible,
            # but potential due to inference) and thus guarantee termination
            # of the while-loop
            yield parent
            parents.add(parent)
            to_explore.extend(parent.ancestors(recurs=False))

