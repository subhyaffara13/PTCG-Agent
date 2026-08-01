
def module_inputs_torch_nn_LPPool2d(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        ModuleInput(
            constructor_input=FunctionInput(2, 2, 2),
            forward_input=FunctionInput(make_input((1, 3, 7, 7)))),
        ModuleInput(
            constructor_input=FunctionInput(2, 2, 2),
            forward_input=FunctionInput(make_input((3, 7, 7))),
            reference_fn=no_batch_dim_reference_fn,
            desc='no_batch_dim'),
        ModuleInput(
            constructor_input=FunctionInput(1.5, 2),
            forward_input=FunctionInput(make_input((1, 3, 7, 7))),
            desc='norm'),
    ]

