
def sample_inputs_constant_pad_nd(op_info, device, dtype, *args, **kwargs):
    # Inherit sample inputs from nn.pad, but transform them to fit
    # constant_pad_nd's interface
    nn_samples = sample_inputs_nn_pad(op_info, device, dtype, *args,
                                      mode='constant', **kwargs)

    # NOTE: primTorch is more strict about the type of the fill value argument
    # So we must cast it to the correct dtype
    from torch._prims_common import dtype_to_type
    scalar_type = dtype_to_type(dtype)

    def drop_mode_argument(input, pad, mode=None, value=None):
        if value is None:
            return SampleInput(input, args=(pad,))
        else:
            return SampleInput(input, args=(pad, scalar_type(value)))

    for sample in nn_samples:
        yield drop_mode_argument(sample.input, *sample.args, **sample.kwargs)

