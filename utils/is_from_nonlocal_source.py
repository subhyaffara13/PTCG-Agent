
def is_from_nonlocal_source(source: Source) -> bool:
    if isinstance(source, ChainedSource):
        return is_from_nonlocal_source(source.base)
    return (
        isinstance(source, LocalSource)
        and source.is_derefed_cell_contents
        and not source.is_input
    )

