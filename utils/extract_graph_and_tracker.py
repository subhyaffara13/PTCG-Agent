
def extract_graph_and_tracker(fn, *args, **kwargs):  # type: ignore[no-untyped-def]
    from torch._dynamo.symbolic_convert import InstructionTranslator

    gm = None
    region_tracker = None

    def extract_graph_backend(_gm, *args, **kwargs):  # type: ignore[no-untyped-def]
        nonlocal gm
        nonlocal region_tracker
        gm = _gm
        region_tracker = InstructionTranslator.current_tx().output.region_tracker
        return _gm

    torch.compile(backend=extract_graph_backend, fullgraph=True)(fn)(*args, **kwargs)
    return gm.graph, region_tracker  # type: ignore[union-attr]

