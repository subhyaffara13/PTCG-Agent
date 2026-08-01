
def mkldnn_rnn_layer(
    input,
    w0,
    w1,
    w2,
    w3,
    hx_,
    cx_,
    reverse,
    batch_sizes,
    mode,
    hidden_size,
    num_layers,
    has_biases,
    bidirectional,
    batch_first,
    train,
):
    seq_length = input.shape[1] if batch_first else input.shape[0]
    mini_batch = input.shape[0] if batch_first else input.shape[1]
    output_chanels = hidden_size
    out_shape = (
        [mini_batch, seq_length, output_chanels]
        if batch_first
        else [seq_length, mini_batch, output_chanels]
    )
    output = input.new_empty(out_shape)
    if hx_ is None:
        hy = torch.empty(0, device=input.device)
    else:
        hy = hx_.new_empty(hx_.shape)
    if cx_ is None:
        cy = torch.empty(0, device=input.device)
    else:
        cy = cx_.new_empty(cx_.shape)
    workspace = torch.empty(0, device=input.device, dtype=torch.uint8)
    return output, hy, cy, workspace

