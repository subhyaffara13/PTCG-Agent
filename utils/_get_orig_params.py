
def _get_orig_params(
    module: nn.Module,
    ignored_params: set[nn.Parameter],
) -> Iterator[nn.Parameter]:
    """
    Return an iterator over the original parameters in ``module``.

    The iterator does not return
    the parameters in ``ignored_params``, any ``FlatParameter`` s (which may be
    present due to nested FSDP wrapping), or any original parameters already
    flattened (only relevant when ``use_orig_params=True``).
    """
    param_gen = module.parameters()
    try:
        while True:
            param = next(param_gen)
            if param not in ignored_params and not _is_fsdp_flattened(param):
                yield param
    except StopIteration:
        pass

