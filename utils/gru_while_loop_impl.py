
def gru_while_loop_impl(
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
    GRU implementation using while_loop for export compatibility.

    This is a drop-in replacement for the default GRU decomposition that uses
    while_loop instead of Python loops, making it more suitable for torch.export.

    Args:
        input: Input tensor
        hx: Hidden state tensor
        params: List of weight and bias tensors
        has_biases: Whether biases are included
        num_layers: Number of GRU layers
        dropout: Dropout probability
        train: Training mode
        bidirectional: Whether to use bidirectional GRU
        batch_first: Whether batch dimension is first

    Returns:
        Tuple of (output, h_n)
    """
    params = gather_params(params, has_biases, False)
    hidden = list(hx.unbind(0))
    layer_fn = one_layer_while_loop_gru
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
    return out, torch.stack(final_hiddens, 0)

