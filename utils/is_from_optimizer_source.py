
def is_from_optimizer_source(source: Source) -> bool:
    if isinstance(source, OptimizerSource):
        return True
    if isinstance(source, ChainedSource):
        return is_from_optimizer_source(source.base)
    return False

