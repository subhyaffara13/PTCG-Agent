
def all_return_statements(node: Node) -> list[ReturnStmt]:
    v = ReturnCollector()
    node.accept(v)
    return v.return_statements

