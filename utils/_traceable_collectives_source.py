
def _traceable_collectives_source(
    tx: "InstructionTranslator", fn: Callable[..., Any]
) -> AttrSource:
    assert torch.distributed.is_available(), "Illegal invocation."
    assert fn in _traceable_collective_remaps().values()

    inner_name = fn.__name__
    path_source = tx.import_source("torch.distributed._functional_collectives")
    return AttrSource(path_source, inner_name)

