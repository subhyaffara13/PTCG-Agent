
def get_resampler(obj: Series | DataFrame, **kwds) -> Resampler:
    """
    Create a TimeGrouper and return our resampler.
    """
    tg = TimeGrouper(obj, **kwds)  # type: ignore[arg-type]
    return tg._get_resampler(obj)

