
def has_recomputable_ops(fx_g: fx.GraphModule) -> bool:
    for node in fx_g.graph.nodes:
        if must_recompute(node):
            return True
    return False

