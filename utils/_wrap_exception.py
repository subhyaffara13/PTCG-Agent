
def _wrap_exception(exc: BaseException) -> WRAPPED_EXCEPTION:
    summary = tb.extract_tb(exc.__traceback__)
    # Python 3.13+ stores bytecode objects in FrameSummary._code,
    # which cannot be pickled. Clear them so gather_object succeeds
    # and the real exception is reported instead of a misleading
    # "cannot pickle code objects" TypeError.
    for frame in summary:
        if hasattr(frame, "_code"):
            object.__setattr__(frame, "_code", None)
    return (exc, summary)

