
def get_mypy_node_for_name(module: str, type_name: str) -> mypy.nodes.SymbolNode | None:
    stub = get_stub(module)
    if stub is None:
        return None
    if type_name not in stub.names:
        return None
    return stub.names[type_name].node

