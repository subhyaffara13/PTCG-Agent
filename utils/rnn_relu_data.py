
def rnn_relu_data(
    data,
    batch_sizes,
    hx,
    params,
    has_biases,
    num_layers,
    dropout,
    train,
    bidirectional,
):
    hidden = hx.unbind(0)
    params = gather_params(params, has_biases, False)
    out, final_hiddens = _rnn_helper(
        data,
        hidden,
        params,
        has_biases,
        num_layers,
        dropout,
        train,
        bidirectional,
        False,
        partial(
            one_layer_rnn_data,
            batch_sizes=batch_sizes,
            hidden_fn=rnn_cell_data(torch.relu),
        ),
    )
    return out, torch.stack(final_hiddens, 0)

