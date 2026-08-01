
def _is_fwd_seed_offset(node: torch.fx.Node) -> bool:
    return node.op == "placeholder" and (
        "fwd_seed" in str(node.target) or "fwd_base_offset" in str(node.target)
    )

