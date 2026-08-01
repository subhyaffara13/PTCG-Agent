
def _is_autocast_sub_mod(node: torch.fx.Node) -> bool:
    """
    Check if the first non-placeholder node is `torch.amp.autocast_mode._enter_autocast`.
    """
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
            and first_non_ph.target is torch.amp.autocast_mode._enter_autocast
        ):
            # TODO: check if current auto-cast type is the same as the args of
            # _enter_autocast. If so, return False, i.e. do not create a submodule.
            return True
    return False

