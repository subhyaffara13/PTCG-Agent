
def is_tf32_warning_applicable(gm: GraphModule) -> bool:
    aten = torch.ops.aten
    tf32_ops = OrderedSet(
        [
            aten.mm.default,
            aten.addmm.default,
            aten.bmm.default,
            aten.baddbmm.default,
        ]
    )
    for target in tf32_ops:
        for node in gm.graph.find_nodes(op="call_function", target=target):
            if (
                isinstance(node.meta.get("val", None), torch.Tensor)
                and node.meta["val"].dtype == torch.float32
                and node.meta["val"].device.type == "cuda"
            ):
                return True
    return False

