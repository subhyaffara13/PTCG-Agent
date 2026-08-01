
def _except_statement_is_always_returning(
    node: nodes.Try, returning_node_class: nodes.NodeNG
) -> bool:
    """Detect if all except statements return."""
    return all(
        any(isinstance(child, returning_node_class) for child in handler.body)
        for handler in node.handlers
    )

