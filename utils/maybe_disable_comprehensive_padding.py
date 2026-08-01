
def maybe_disable_comprehensive_padding(
    example_inputs: Sequence[InputType],
) -> AbstractContextManager[None, None]:
    """
    For CPU backend, enable comprehensive padding causes some unit tests
    fail due to changing number of generated kernels. Skip for now.
    """
    has_gpu = any(
        is_gpu(t.device.type) for t in example_inputs if isinstance(t, torch.Tensor)
    )

    if config.disable_padding_cpu and config.comprehensive_padding and not has_gpu:
        perf_hint_log.info("Skip comprehensive padding on CPU")
        return config.patch(comprehensive_padding=False)
    elif config.aot_inductor.use_runtime_constant_folding:
        perf_hint_log.info(
            "Skip comprehensive padding for use_runtime_constant_folding"
        )
        return config.patch(comprehensive_padding=False)
    else:
        return contextlib.nullcontext()

