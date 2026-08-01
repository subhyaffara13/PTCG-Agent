
def replace_random_passes(gm: torch.fx.GraphModule):
    """Modify the given FX graph to use backend-native random ops"""
    if config.fallback_random:
        return 0

    count = patterns.apply(gm)
    with GraphTransformObserver(gm, "fuse_seed_creation_pass", "joint_graph_passes"):
        count += fuse_seed_creation_pass(gm.graph)
    if config.align_random_eager:
        with GraphTransformObserver(gm, "fuse_offset_creation_pass"):
            count += fuse_offset_creation_pass(gm.graph)

    return count

