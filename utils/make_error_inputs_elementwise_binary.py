
def make_error_inputs_elementwise_binary(error_inputs_func):
    def error_inputs_func_wrapper(op, device, **kwargs):
        if error_inputs_func is not None:
            yield from error_inputs_func(op, device, **kwargs)

        if not op.supports_rhs_python_scalar:
            si = SampleInput(torch.tensor((1, 2, 3), device=device), args=(2,))
            yield ErrorInput(si, error_type=Exception, error_regex="")

        if not op.supports_one_python_scalar:
            si = SampleInput(2, args=(torch.tensor((1, 2, 3), device=device),))
            yield ErrorInput(si, error_type=Exception, error_regex="")

        if (
            not kwargs.get("skip_two_python_scalars", False)
            and not op.supports_two_python_scalars
        ):
            si = SampleInput(2, args=(3,))
            yield ErrorInput(si, error_type=Exception, error_regex="")

    return error_inputs_func_wrapper

