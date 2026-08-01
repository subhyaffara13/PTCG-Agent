
def _get_filtered_node_statements(
    base_node: nodes.NodeNG, stmt_nodes: list[nodes.NodeNG]
) -> list[tuple[nodes.NodeNG, _base_nodes.Statement]]:
    statements = [(node, node.statement()) for node in stmt_nodes]
    # Next we check if we have ExceptHandlers that are parent
    # of the underlying variable, in which case the last one survives
    if len(statements) > 1 and all(
        isinstance(stmt, nodes.ExceptHandler) for _, stmt in statements
    ):
        statements = [
            (node, stmt) for node, stmt in statements if stmt.parent_of(base_node)
        ]
    return statements

