
def module_inputs_torch_nn_LSTMCell(module_info, device, dtype, requires_grad, training, **kwargs):
    # Currently all samples below are for validating the no-batch-dim support.
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    samples = (
        ModuleInput(
            constructor_input=FunctionInput(5, 10),
            forward_input=FunctionInput(make_input(5), (make_input(10), make_input(10))),
            reference_fn=no_batch_dim_reference_lstmcell,
        ),
        ModuleInput(
            constructor_input=FunctionInput(5, 10, bias=True),
            forward_input=FunctionInput(make_input(5), (make_input(10), make_input(10))),
            reference_fn=no_batch_dim_reference_lstmcell,
        ),
    )

    return samples

