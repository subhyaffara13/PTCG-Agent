
def load_tree(node: MypyFile, options: Options) -> list[ParseError]:
    """Deserialize full AST from serialized raw data."""
    assert node.raw_data is not None
    state = State(options)
    data = ReadBuffer(node.raw_data.defs)
    n = read_int(data)
    node.defs = read_statements(state, data, n)
    node.imports = deserialize_imports(node.raw_data.imports)
    node.raw_data = None
    return state.errors

