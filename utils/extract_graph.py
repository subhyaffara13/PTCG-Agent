
def extract_graph(fn, *args, **kwargs):  # type: ignore[no-untyped-def]
    backend = AotEagerAndRecordGraphs()
    result = torch.compile(backend=backend)(fn)(*args, **kwargs)
    return result, backend.graphs, backend.fw_graphs, backend.bw_graphs

