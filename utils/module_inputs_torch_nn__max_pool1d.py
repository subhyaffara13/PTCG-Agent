
def module_inputs_torch_nn_MaxPool1d(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        ModuleInput(
            constructor_input=FunctionInput(4),
            forward_input=FunctionInput(make_input((2, 10, 4))),
            desc='3d_input'),
        ModuleInput(
            constructor_input=FunctionInput(4, 4),
            forward_input=FunctionInput(make_input((2, 10, 4))),
            desc='stride'),
        ModuleInput(
            constructor_input=FunctionInput(4, return_indices=True),
            forward_input=FunctionInput(make_input((2, 10, 4))),
            desc='return_indices'),
    ]

