
def one_layer_while_loop_lstm(inp, hidden, params, has_biases, reverse=False):
    """
    1 layer fn for while loop LSTM

    Args:
        inp: Input tensor of shape (seq_len, batch, input_size)
        hidden: Tuple of (hx, cx) hidden states
        params: List of weight and bias tensors
        has_biases: Whether biases are included
        reverse: Whether to process sequence in reverse

    Returns:
        Tuple of (output, (final_hx, final_cx))
    """
    ih_weight = params[0]
    hh_weight = params[1]
    ih_bias = params[2] if has_biases else None
    hh_bias = params[3] if has_biases else None
    hr_weight = (
        params[4] if len(params) == 5 else params[2] if len(params) == 3 else None
    )

    hx = hidden[0].unsqueeze(0)
    cx = hidden[1].unsqueeze(0)

    precomputed_input = torch.nn.functional.linear(inp, ih_weight, ih_bias)
    precomputed_input = precomputed_input.flip(0) if reverse else precomputed_input

    # while loop rewrite
    step_output = torch.empty(
        precomputed_input.size(0),
        *tuple(hx.shape[1:]),
        dtype=hx.dtype,
        device=hx.device,
    )

    def cond_fn(i, out, hx, cx):
        return i < precomputed_input.size(0)

    def body_fn(idx, out, hx, cx):
        # Extract the integer value from idx and constrain it for data-dependent indexing
        i = idx.item()
        torch._check_is_size(i)
        torch._check_is_size(i, max=precomputed_input.size(0) - 1)
        hx, cx = lstm_cell(
            precomputed_input[i], hx, cx, hh_weight, hh_bias, hr_weight, chunk_dim=2
        )
        out = out.clone()
        # Squeeze the first dimension before storing (lstm_cell preserves the unsqueezed dim)
        out[i] = hx.squeeze(0)
        return idx + 1, out, hx, cx

    cnt = torch.tensor(0, dtype=torch.int64)
    _, out, final_hx, final_cx = while_loop(
        cond_fn, body_fn, [cnt, step_output, hx, cx]
    )
    if reverse:
        out = out.flip(0)

    # Use squeeze(1) to match original implementation
    return out, (final_hx.squeeze(1), final_cx.squeeze(1))

