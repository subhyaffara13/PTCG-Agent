
def draw_graph(
    traced: torch.fx.GraphModule,
    fname: str,
    figname: str = "fx_graph",
    clear_meta: bool = True,
    prog: str | list[str] | None = None,
    parse_stack_trace: bool = False,
    dot_graph_shape: str | None = None,
) -> None:
    if clear_meta:
        new_graph = copy.deepcopy(traced.graph)
        traced = fx.GraphModule(traced, new_graph)
        for node in traced.graph.nodes:
            node.meta = {}  # pyrefly: ignore[implicit-any]
    base, ext = os.path.splitext(fname)
    if not ext:
        ext = "." + config.torch_compile_graph_format
    log.info("Writing FX graph to file: %s%s", base, ext)
    g = graph_drawer.FxGraphDrawer(
        traced,
        figname,
        parse_stack_trace=parse_stack_trace,
        dot_graph_shape=dot_graph_shape,
    )
    x = g.get_main_dot_graph()
    write_method = getattr(x, "write_" + ext.lstrip("."))
    fname = f"{base}{ext}"
    if prog is None:
        write_method(fname)
    else:
        write_method(fname, prog=prog)

