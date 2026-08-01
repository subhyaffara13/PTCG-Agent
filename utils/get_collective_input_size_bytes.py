
def get_collective_input_size_bytes(node: ir.IRNode) -> int:
    sz_bytes = 0
    for inp in node.inputs:  # type: ignore[attr-defined]
        numel = get_ir_node_size_numel(inp.layout.size)
        sz_bytes += numel * get_dtype_size(inp.layout.dtype)
    return sz_bytes

