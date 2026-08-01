
def is_all_gather_into_tensor(node: torch.fx.Node) -> bool:  # type: ignore[arg-type]
    return node.op == "call_function" and (
        node.target == torch.ops._c10d_functional.all_gather_into_tensor.default
        or node.target == torch.ops._c10d_functional.all_gather_into_tensor_out.default
    )

