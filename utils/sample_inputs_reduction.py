
def sample_inputs_reduction(op_info, device, dtype, requires_grad, **kwargs):
    """Sample inputs for reduction operators."""

    # TODO(@heitorschueroff) Once all reduction operators are using
    # ReductionOpInfo use op_info.supports_multiple_dims directly.
    supports_multiple_dims: bool = kwargs.get("supports_multiple_dims", True)

    # TODO(@heitorschueroff) Once all reduction operators are using ReductionOpInfo
    # use op_info.generate_args_kwargs directly.
    generate_args_kwargs = kwargs.get(
        "generate_args_kwargs", lambda *args, **kwargs: (yield (), {})
    )

    for t in _generate_reduction_inputs(device, dtype, requires_grad):
        for reduction_kwargs in _generate_reduction_kwargs(
            t.ndim, supports_multiple_dims
        ):
            for args, kwargs in generate_args_kwargs(t, **reduction_kwargs):
                kwargs.update(reduction_kwargs)
                yield SampleInput(
                    t.detach().requires_grad_(requires_grad), args=args, kwargs=kwargs
                )

