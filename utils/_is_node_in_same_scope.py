
def _is_node_in_same_scope(
    candidate: nodes.NodeNG, node_scope: nodes.LocalsDictNodeNG
) -> bool:
    if isinstance(candidate, (nodes.ClassDef, nodes.FunctionDef)):
        return candidate.parent is not None and candidate.parent.scope() is node_scope
    return candidate.scope() is node_scope

