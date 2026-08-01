
def is_from_closure_source(source: Source) -> bool:
    if isinstance(source, ClosureSource):
        return True
    if isinstance(source, ChainedSource):
        return is_from_closure_source(source.base)
    return False

