
def _preserve_node_seq_nr(preserve_seq_nr: bool = True) -> Iterator[None]:
    """
    Temporarily enables or disables the preservation of node.meta["seq_nr"] in the
    tracing context.
    """
    global _should_preserve_node_meta
    saved = _should_preserve_node_meta

    try:
        _should_preserve_node_meta = preserve_seq_nr
        yield
    finally:
        _should_preserve_node_meta = saved

