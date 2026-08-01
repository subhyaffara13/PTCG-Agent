
def _get_graph_module_cls() -> type[GraphModule]:
    return _LazyGraphModule if _use_lazy_graph_module_flag else GraphModule

