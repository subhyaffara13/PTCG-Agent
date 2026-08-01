
def module_inputs_torch_nn_RNN_GRU_Cell(module_info, device, dtype, requires_grad, training, **kwargs):
    # Currently all samples below are for validating the no-batch-dim support.
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    samples = [
        ModuleInput(
            constructor_input=FunctionInput(5, 10),
            forward_input=FunctionInput(make_input(5), make_input(10)),
            reference_fn=no_batch_dim_reference_fn,
        ),
        ModuleInput(
            constructor_input=FunctionInput(5, 10, bias=True),
            forward_input=FunctionInput(make_input(5), make_input(10)),
            reference_fn=no_batch_dim_reference_fn,
        )
    ]

    is_rnn = kwargs.get('is_rnn', False)
    if is_rnn:
        # RNN also supports `nonlinearity` argument.
        # `tanh` is the default, so we check with `relu`
        samples.append(
            ModuleInput(
                constructor_input=FunctionInput(5, 10, bias=True, nonlinearity='relu'),
                forward_input=FunctionInput(make_input(5), make_input(10)),
                reference_fn=no_batch_dim_reference_fn,
            )
        )

    return samples

