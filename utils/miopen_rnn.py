
def miopen_rnn(
    input,
    weight,
    weight_stride0,
    # weight_buf,
    hx,
    cx,
    mode,
    hidden_size,
    # proj_size,
    num_layers,
    batch_first,
    dropout,
    train,
    bidirectional,
    batch_sizes,
    dropout_state,
):
    total_weight_elems = 0
    for w in weight:
        if w.numel() > 0:
            total_weight_elems += w.numel()

    weight_buf = input.new_empty((total_weight_elems,))
    return _cudnn_rnn(
        input,
        weight,
        weight_stride0,
        weight_buf,
        hx,
        cx,
        mode,
        hidden_size,
        0,
        num_layers,
        batch_first,
        dropout,
        train,
        bidirectional,
        batch_sizes,
        dropout_state,
    )

