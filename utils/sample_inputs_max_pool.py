
def sample_inputs_max_pool(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=False)

    params_generator_type_dict = {
        'nn.functional.max_pool1d': _TestParamsMaxPool1d,
        'nn.functional.max_pool2d': _TestParamsMaxPool2d,
        'nn.functional.max_pool3d': _TestParamsMaxPool3d,
        'max_pool2d_with_indices_backward': _TestParamsMaxPool2d,
    }

    params_generator = params_generator_type_dict[op_info.name]()
    for (shape, memory_format), kwargs in params_generator.gen_input_params():
        arg = make_arg(shape).to(memory_format=memory_format).requires_grad_(requires_grad)
        yield SampleInput(arg, kwargs=kwargs)

