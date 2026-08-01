
def module_inputs_torch_nn_MaxPool3d(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        ModuleInput(
            constructor_input=FunctionInput((2, 2, 2)),
            forward_input=FunctionInput(make_input((2, 3, 5, 5, 5)))),
        ModuleInput(
            constructor_input=FunctionInput(2, (2, 2, 2)),
            forward_input=FunctionInput(make_input((2, 3, 5, 5, 5))),
            desc='stride'),
        ModuleInput(
            constructor_input=FunctionInput(2, 2, (1, 1, 1)),
            forward_input=FunctionInput(make_input((2, 3, 5, 5, 5))),
            desc='stride_padding'),
        ModuleInput(
            constructor_input=FunctionInput(2, 2, (1, 1, 1), return_indices=True),
            forward_input=FunctionInput(make_input((2, 3, 5, 5, 5))),
            desc='return_indices'),
    ]

