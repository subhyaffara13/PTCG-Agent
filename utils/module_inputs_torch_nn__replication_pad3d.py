
def module_inputs_torch_nn_ReplicationPad3d(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        ModuleInput(
            constructor_input=FunctionInput(1),
            forward_input=FunctionInput(make_input((3, 4, 5, 6))),
            reference_fn=no_batch_dim_reference_fn,
        ),
        ModuleInput(
            constructor_input=FunctionInput((1, 2, 3, 4, 5, 6)),
            forward_input=FunctionInput(make_input((3, 4, 5, 6, 7))),
        ),
    ]

