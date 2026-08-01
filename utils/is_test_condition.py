
def is_test_condition(
    node: nodes.NodeNG,
    parent: nodes.NodeNG | None = None,
) -> bool:
    """Returns true if the given node is being tested for truthiness."""
    match parent := parent or node.parent:
        case nodes.While() | nodes.If() | nodes.IfExp() | nodes.Assert():
            return node is parent.test or parent.test.parent_of(node)
        case nodes.Comprehension():
            return node in parent.ifs
    return is_call_of_name(parent, "bool") and parent.parent_of(node)

