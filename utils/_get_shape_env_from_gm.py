
def _get_shape_env_from_gm(gm: torch.fx.GraphModule):
    vals = [
        node.meta["val"]
        for node in gm.graph.nodes
        if node.meta.get("val", None) is not None
    ]

    fake_mode = _detect_fake_mode_from_gm(gm)
    if fake_mode is not None:
        return fake_mode.shape_env
    for v in vals:
        if isinstance(v, torch.SymInt):
            return v.node.shape_env

