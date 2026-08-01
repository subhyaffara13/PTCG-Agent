
def _is_bwd_seed_offset(node: torch.fx.Node) -> bool:
    return node.op == "placeholder" and (
        "bwd_seed" in str(node.target) or "bwd_base_offset" in str(node.target)
    )

