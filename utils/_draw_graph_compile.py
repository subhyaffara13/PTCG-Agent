
def _draw_graph_compile(
    fx_g: fx.GraphModule, _: Any, name: str, clear_meta: bool = True
) -> fx.GraphModule:
    print(fx_g.code)
    draw_graph(fx_g, name, clear_meta=clear_meta)
    return fx_g

