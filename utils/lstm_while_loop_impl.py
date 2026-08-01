
def lstm_while_loop_impl(
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
    """
    LSTM implementation using while_loop for export compatibility.

    This is a drop-in replacement for the default LSTM decomposition that uses
    while_loop instead of Python loops, making it more suitable for torch.export.

    Args:
        input: Input tensor
        hx: Tuple of (h0, c0) hidden states
        params: List of weight and bias tensors
        has_biases: Whether biases are included
        num_layers: Number of LSTM layers
        dropout: Dropout probability
        train: Training mode
        bidirectional: Whether to use bidirectional LSTM
        batch_first: Whether batch dimension is first

    Returns:
        Tuple of (output, h_n, c_n)
    """
    if len(hx) != 2:
        raise AssertionError("lstm expects two hidden states")
    params = gather_params(params, has_biases, hx[0].size(2) != hx[1].size(2))
    hidden = list(zip(hx[0], hx[1]))
    layer_fn = one_layer_while_loop_lstm
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
        layer_fn,
    )
    final_hiddens = list(zip(*final_hiddens))
    return out, torch.stack(final_hiddens[0], 0), torch.stack(final_hiddens[1], 0)

