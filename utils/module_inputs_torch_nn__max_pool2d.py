
def module_inputs_torch_nn_MaxPool2d(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        ModuleInput(
            constructor_input=FunctionInput((3, 3), (2, 2), (1, 1)),
            forward_input=FunctionInput(make_input((3, 7, 7))),
            desc='3d_input'),
        ModuleInput(
            constructor_input=FunctionInput((3, 3), (2, 2), (1, 1)),
            forward_input=FunctionInput(make_input((1, 3, 7, 7))),
            desc='4d_input'),
        ModuleInput(
            constructor_input=FunctionInput((3, 3), (2, 2), (1, 1), return_indices=True),
            forward_input=FunctionInput(make_input((1, 3, 7, 7))),
            desc='return_indices'),
    ]

