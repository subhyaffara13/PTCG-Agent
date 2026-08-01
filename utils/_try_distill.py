
def _try_distill(func, tmppath, *args, **kwargs):
    try:
        func(str(tmppath), *args, **kwargs)
    except mpl.ExecutableNotFoundError as exc:
        _log.warning("%s.  Distillation step skipped.", exc)

