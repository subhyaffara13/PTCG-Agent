
def _use_lazy_graph_module(should_use: bool) -> Iterator[None]:
    try:
        global _use_lazy_graph_module_flag
        prior = _use_lazy_graph_module_flag
        _use_lazy_graph_module_flag = (
            should_use and not _force_skip_lazy_graph_module_flag
        )
        yield
    finally:
        _use_lazy_graph_module_flag = prior

