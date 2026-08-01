
def has_mergeable_all_gather_convert_dtype(n: torch.fx.Node) -> bool:
    node_in = n.args[0]
    return (
        is_all_gather_into_tensor(n)
        and isinstance(node_in, torch.fx.Node)
        and node_in.op == "call_function"
        and (
            node_in.target is torch.ops.prims.convert_element_type.default
            or node_in.target is torch.ops.aten._to_copy.default
        )
        and len(node_in.users) == 1
    )

