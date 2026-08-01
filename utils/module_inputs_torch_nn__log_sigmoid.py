
def module_inputs_torch_nn_LogSigmoid(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        ModuleInput(
            constructor_input=FunctionInput(),
            forward_input=FunctionInput(make_input(())),
            reference_fn=lambda m, p, i: i.sigmoid().log(),
            desc='scalar'
        ),
        ModuleInput(
            constructor_input=FunctionInput(),
            forward_input=FunctionInput(make_input((2, 3, 4))),
            reference_fn=lambda m, p, i: i.sigmoid().log(),
        ),
        ModuleInput(
            constructor_input=FunctionInput(),
            forward_input=FunctionInput(make_input(4)),
            reference_fn=no_batch_dim_reference_fn,
            desc='no_batch_dim',
        ),
    ]

