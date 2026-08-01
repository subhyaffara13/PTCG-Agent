
def has_recomputable_rng_ops(fx_g: fx.GraphModule) -> bool:
    for node in fx_g.graph.nodes:
        if (
            must_recompute(node)
            and hasattr(node.target, "tags")
            and torch.Tag.nondeterministic_seeded in node.target.tags
        ):
            return True
    return False

