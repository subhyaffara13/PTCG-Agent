from typing import Any, Callable

def run_and_get_graph_lowering(
    fn: Callable[P, _T], *args: P.args, **kwargs: P.kwargs
) -> tuple[Any, list[GraphLowering]]:
    from torch._inductor.graph import GraphLowering
    from torch._inductor.output_code import CompiledFxGraph

    real_init = CompiledFxGraph.__init__
    graph_lowerings = []

    def fake_init(*args: Any, **kwargs: Any) -> None:
        real_init(*args, **kwargs)
        graph = args[2]
        assert isinstance(graph, GraphLowering)
        graph_lowerings.append(graph)

    with mock.patch.object(CompiledFxGraph, "__init__", fake_init):
        result = fn(*args, **kwargs)

    return result, graph_lowerings

