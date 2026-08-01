
def _lstm_full(
    g: jit_utils.GraphContext,
    input,
    hidden_v,
    weight_v,
    has_biases,
    num_layers,
    dropout,
    train,
    bidirectional,
    batch_first,
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
        batch_first,
    )

