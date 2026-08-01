
def _as_overlapped_optim(optim_cls: type, params, *args, **kwargs):
    """Return a new ``OverlappedOptimizer`` instance that supports ``optim_cls``."""
    for clz in inspect.getmro(optim_cls):
        try:
            return _registered_overlapped_optims[clz](
                optim_cls, params, *args, **kwargs
            )
        except KeyError:
            pass

    # Fallback to standard overlapped optimizer, which will raise errors if user
    # is attempting to use an unsupported optimizer.
    return _OverlappedStandardOptimizer(optim_cls, params, *args, **kwargs)

