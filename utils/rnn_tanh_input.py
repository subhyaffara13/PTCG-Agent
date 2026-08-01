
def rnn_tanh_input(
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
    hidden = hx.unbind(0)
    params = gather_params(params, has_biases, False)
    out, final_hiddens = _rnn_helper(
        input,
        hidden,
        params,
        has_biases,
        num_layers,
        dropout,
        train,
        bidirectional,
        batch_first,
        partial(one_layer_rnn, hidden_fn=rnn_cell(torch.tanh)),
    )
    return out, torch.stack(final_hiddens, 0)

