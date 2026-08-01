
def filter_excinfo_traceback(
    tbfilter: TracebackFilter, excinfo: ExceptionInfo[BaseException]
) -> Traceback:
    """Filter the exception traceback in ``excinfo`` according to ``tbfilter``."""
    if callable(tbfilter):
        return tbfilter(excinfo)
    elif tbfilter:
        return excinfo.traceback.filter(excinfo)
    else:
        return excinfo.traceback

