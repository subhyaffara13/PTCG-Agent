
def get_first_incompatible_cudagraph_node(
    gm: torch.fx.GraphModule,
) -> torch.fx.Node | None:
    from torch.fx.experimental.symbolic_shapes import free_unbacked_symbols

    for node in gm.graph.nodes:
        if is_cudagraph_unsafe_fx_node(node):
            return node

        if (val := node.meta.get("val")) is not None and free_unbacked_symbols(val):
            return node

    return None

