
def _normalize_shuffle_graph(shuffle_gm: torch.fx.GraphModule) -> None:
    shuffle_gm.graph.eliminate_dead_code()
    shuffle_gm.recompile()
    for name, buffer in list(shuffle_gm.named_buffers()):
        delattr(shuffle_gm, name)
        setattr(shuffle_gm, name, buffer)

