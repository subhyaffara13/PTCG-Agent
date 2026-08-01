
def module_inputs_torch_nn_RNN_GRU(module_info, device, dtype, requires_grad, training, with_packed_sequence=False, **kwargs):
    # Currently all samples below are for validating the no-batch-dim support.
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    is_rnn = kwargs['is_rnn']
    nonlinearity = ('relu', 'tanh')
    bias = (False, True)
    batch_first = (False, True)
    bidirectional = (False, True)

    samples = []
    if is_rnn:
        prod_gen = product(nonlinearity, bias, batch_first, bidirectional)
    else:
        prod_gen = product(bias, batch_first, bidirectional)

    for args in prod_gen:
        if is_rnn:
            nl, b, b_f, bidir = args
        else:
            b, b_f, bidir = args

        cons_args = {'input_size': 2, 'hidden_size': 2, 'num_layers': 2,
                     'batch_first': b_f, 'bias': b, 'bidirectional': bidir}
        cons_args_hidden = {'input_size': 2, 'hidden_size': 3, 'num_layers': 2,
                            'batch_first': b_f, 'bias': b, 'bidirectional': bidir}

        if is_rnn:
            cons_args['nonlinearity'] = nl
            cons_args_hidden['nonlinearity'] = nl
        samples.append(
            ModuleInput(
                constructor_input=FunctionInput(**cons_args),
                forward_input=FunctionInput(make_input((3, 2))),
                reference_fn=partial(no_batch_dim_reference_rnn_gru, batch_first=b_f),
            )
        )
        samples.append(
            ModuleInput(
                constructor_input=FunctionInput(**cons_args_hidden),
                forward_input=FunctionInput(make_input((3, 2)), make_input((4 if bidir else 2, 3))),
                reference_fn=partial(no_batch_dim_reference_rnn_gru, batch_first=b_f),
            )
        )
        if with_packed_sequence:
            samples.append(
                ModuleInput(
                    constructor_input=FunctionInput(**cons_args),
                    forward_input=FunctionInput(make_packed_sequence(make_input((5, 2, 2)), torch.tensor([5, 3]))),
                    reference_fn=partial(no_batch_dim_reference_rnn_gru, batch_first=b_f),
                )
            )
            samples.append(
                ModuleInput(
                    constructor_input=FunctionInput(**cons_args),
                    forward_input=FunctionInput(make_packed_sequence(make_input((5, 5, 2)), torch.tensor([5, 3, 3, 2, 2]))),
                    reference_fn=partial(no_batch_dim_reference_rnn_gru, batch_first=b_f),
                )
            )

    return samples

