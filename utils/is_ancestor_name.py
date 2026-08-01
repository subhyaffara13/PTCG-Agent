
def is_ancestor_name(frame: nodes.ClassDef, node: nodes.NodeNG) -> bool:
    """Return whether `frame` is an nodes.Class node with `node` in the
    subtree of its bases attribute.
    """
    if not isinstance(frame, nodes.ClassDef):
        return False
    return any(node in base.nodes_of_class(nodes.Name) for base in frame.bases)

