
def _unpack_list(list_value: _C.Value) -> list[_C.Value]:
    list_node = list_value.node()
    if list_node.kind() != "prim::ListConstruct":
        raise errors.SymbolicValueError(
            f"ONNX symbolic expected node type prim::ListConstruct, got '{list_node}'.",
            list_value,
        )
    return list(list_node.inputs())

