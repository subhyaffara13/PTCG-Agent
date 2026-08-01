
def draw_graph_compile(
    name: str,
) -> Callable[[fx.GraphModule, list[Any]], fx.GraphModule]:
    return make_boxed_compiler(partial(_draw_graph_compile, name=name))

