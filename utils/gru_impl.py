
def gru_impl(
    input,
    hx,
    params,
    has_biases,
    num_layers,
    dropout,
    train,
    bidirectional,
    batch_first,
):
    params = gather_params(params, has_biases, False)
    out, final_hiddens = _rnn_helper(
        input,
        hx.unbind(0),
        params,
        has_biases,
        num_layers,
        dropout,
        train,
        bidirectional,
        batch_first,
        partial(one_layer_rnn, hidden_fn=gru_cell),
    )
    return out, torch.stack(final_hiddens, 0)

