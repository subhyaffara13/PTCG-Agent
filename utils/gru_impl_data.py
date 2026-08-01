
def gru_impl_data(
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
    params = gather_params(params, has_biases, False)
    out, final_hiddens = _rnn_helper(
        data,
        hx.unbind(0),
        params,
        has_biases,
        num_layers,
        dropout,
        train,
        bidirectional,
        False,
        partial(one_layer_rnn_data, batch_sizes=batch_sizes, hidden_fn=gru_cell_data),
    )
    return out, torch.stack(final_hiddens, 0)

