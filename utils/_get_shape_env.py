
def _get_shape_env(gm):
    vals = [
        node.meta["val"]
        for node in gm.graph.nodes
        if node.meta.get("val", None) is not None
    ]
    from torch._guards import detect_fake_mode

    fake_mode = detect_fake_mode(vals)
    if fake_mode is not None:
        return fake_mode.shape_env
    for v in vals:
        if isinstance(v, torch.SymInt):
            return v.node.shape_env

