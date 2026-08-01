
def module_inputs_torch_nn_LSTM(module_info, device, dtype, requires_grad, training, **kwargs):
    # Currently all samples below are for validating the no-batch-dim support.
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    bias = (False, True)
    batch_first = (False, True)
    bidirectional = (False, True)
    proj_sizes = (0, 2)

    samples = []
    prod_gen = product(bias, batch_first, bidirectional, proj_sizes)

    for args in prod_gen:
        b, b_f, bidir, proj_size = args
        hidden_size = 3
        cons_args = {'input_size': 2, 'hidden_size': hidden_size, 'num_layers': 2, 'proj_size': proj_size,
                     'batch_first': b_f, 'bias': b, 'bidirectional': bidir}
        cons_args_hidden = {'input_size': 2, 'hidden_size': hidden_size, 'num_layers': 2, 'proj_size': proj_size,
                            'batch_first': b_f, 'bias': b, 'bidirectional': bidir}

        samples.append(
            ModuleInput(
                constructor_input=FunctionInput(**cons_args),
                forward_input=FunctionInput(make_input((2, 2))),
                reference_fn=partial(no_batch_dim_reference_lstm, batch_first=b_f),
            )
        )

        h_out = proj_size if proj_size > 0 else hidden_size
        hx = (make_input((4 if bidir else 2, h_out)), make_input((4 if bidir else 2, hidden_size)))
        samples.append(
            ModuleInput(
                constructor_input=FunctionInput(**cons_args_hidden),
                forward_input=FunctionInput(make_input((3, 2)), hx),
                reference_fn=partial(no_batch_dim_reference_lstm, batch_first=b_f),
            )
        )


    return samples

