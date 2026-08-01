
def _lstm_packed(
    g: jit_utils.GraphContext,
    input,
    batch_sizes,
    hidden_v,
    weight_v,
    has_biases,
    num_layers,
    dropout,
    train,
    bidirectional,
):
    hidden, weight = (
        symbolic_helper._unpack_list(hidden_v),
        symbolic_helper._unpack_list(weight_v),
    )
    return _generic_rnn(
        g,
        "LSTM",
        input,
        hidden,
        weight,
        has_biases,
        num_layers,
        dropout,
        train,
        bidirectional,
        batch_sizes=batch_sizes,
    )

