
def buf_name_to_fused_snode(
    buf_name: str, name_to_buf: dict[str, Any], name_to_fused_node: dict[str, Any]
) -> Any:
    return name_to_fused_node[name_to_buf[buf_name].defining_op.get_name()]

