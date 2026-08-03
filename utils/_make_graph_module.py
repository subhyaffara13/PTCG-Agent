from typing import Any

def _make_graph_module(
    *args: Any, graph_module_cls: type[GraphModule] | None = None, **kwargs: Any
) -> GraphModule:
    if graph_module_cls is None:
        graph_module_cls = _get_graph_module_cls()

    return graph_module_cls(*args, **kwargs)

