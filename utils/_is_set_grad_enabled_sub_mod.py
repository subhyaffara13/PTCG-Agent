
def _is_set_grad_enabled_sub_mod(
    node: torch.fx.Node, omit_if_same_with_ambient: bool = False
) -> bool | torch.Tensor:
    if node.op == "call_module":
        if not isinstance(node.target, str):
            raise AssertionError(f"expected str target, got {type(node.target)}")
        subgm = getattr(node.graph.owning_module, node.target)
        first_non_ph = nodes_first(
            subgm.graph.nodes, lambda node: node.op != "placeholder"
        )
        if (
            first_non_ph
            and first_non_ph.op == "call_function"
            and first_non_ph.target is torch._C._set_grad_enabled
        ):
            return (
                first_non_ph.args[0] != torch.is_grad_enabled()
                if omit_if_same_with_ambient
                else True
            )
    return False

