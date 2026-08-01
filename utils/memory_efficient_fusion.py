
def memory_efficient_fusion(
    fn: Callable[_P, _R] | nn.Module,
    **kwargs: Any,
) -> Callable[_P, _R] | nn.Module:
    """
    Wrapper function over :func:`aot_function` and :func:`aot_module` to perform
    memory efficient fusion. It uses the
    :func:`min_cut_rematerialization_partition` partitioner to perform efficient
    recomputation. It uses NVFuser to compile the generated forward and backward
    graphs.

    .. warning::
        This API is experimental and likely to change.

    Args:
        fn (Union[Callable, nn.Module]): A Python function or a ``nn.Module``
            that takes one or more arguments. Must return one or more Tensors.
        **kwargs: Any other overrides you want to make to the settings

    Returns:
        Returns a ``Callable``  or ``nn.Module`` that retains the eager behavior
        of the original :attr:`fn`, but whose forward and backward graphs have
        gone through recomputation optimizations, and the graphs have been
        compiled with nvfuser.

    """
    config = {
        "fw_compiler": ts_compile,
        "bw_compiler": ts_compile,
        "partition_fn": min_cut_rematerialization_partition,
        "decompositions": default_decompositions,
    }
    config.update(kwargs)
    if isinstance(fn, torch.nn.Module):
        return aot_module(fn, **config)  # pyrefly: ignore[bad-argument-type]
    else:
        return aot_function(fn, **config)  # pyrefly: ignore[bad-argument-type]

