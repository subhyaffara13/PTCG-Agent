
def module_inputs_torch_nn_AvgPool2d(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        ModuleInput(constructor_input=FunctionInput((2, 2)),
                    forward_input=FunctionInput(make_input((3, 6, 6))),
                    desc='no_batch_dim',
                    reference_fn=no_batch_dim_reference_fn),
        ModuleInput(constructor_input=FunctionInput((2, 2)),
                    forward_input=FunctionInput(make_input((2, 3, 6, 6)))),
        ModuleInput(constructor_input=FunctionInput((2, 2), (2, 2)),
                    forward_input=FunctionInput(make_input((2, 3, 6, 6))),
                    desc='stride'),
        ModuleInput(constructor_input=FunctionInput((2, 2), (2, 2), (1, 1)),
                    forward_input=FunctionInput(make_input((2, 3, 6, 6))),
                    desc='stride_pad'),
        ModuleInput(constructor_input=FunctionInput((2, 2), divisor_override=1),
                    forward_input=FunctionInput(make_input((2, 3, 6, 6))),
                    desc='divisor'),
        ModuleInput(constructor_input=FunctionInput((2, 2), (2, 2), divisor_override=1),
                    forward_input=FunctionInput(make_input((2, 3, 6, 6))),
                    desc='divisor_stride'),
        ModuleInput(constructor_input=FunctionInput((2, 2), (2, 2), (1, 1), divisor_override=1),
                    forward_input=FunctionInput(make_input((2, 3, 6, 6))),
                    desc='divisor_stride_pad')]

