
def one_layer_while_loop_gru(inp, hidden, params, has_biases, reverse=False):
    """
    1 layer fn for while loop GRU

    Args:
        inp: Input tensor of shape (seq_len, batch, input_size)
        hidden: Hidden state tensor
        params: List of weight and bias tensors
        has_biases: Whether biases are included
        reverse: Whether to process sequence in reverse

    Returns:
        Tuple of (output, final_hidden)
    """
    ih_weight = params[0]
    hh_weight = params[1]
    ih_bias = params[2] if has_biases else None
    hh_bias = params[3] if has_biases else None

    precomputed_input = torch.nn.functional.linear(inp, ih_weight, ih_bias)
    precomputed_input = precomputed_input.flip(0) if reverse else precomputed_input
    cur_hidden = hidden.unsqueeze(0)

    # while loop rewrite
    step_output = torch.empty(
        precomputed_input.size(0),
        *tuple(cur_hidden.shape[1:]),
        dtype=cur_hidden.dtype,
        device=cur_hidden.device,
    )

    def cond_fn(i, out, cur_hidden):
        return i < precomputed_input.size(0)

    def body_fn(idx, out, cur_hidden):
        # Extract the integer value from idx and constrain it for data-dependent indexing
        i = idx.item()
        torch._check_is_size(i)
        torch._check_is_size(i, max=precomputed_input.size(0) - 1)
        cur_hidden = gru_cell(
            precomputed_input[i], cur_hidden, ih_weight, ih_bias, hh_weight, hh_bias
        )
        out = out.clone()
        out[i] = cur_hidden.squeeze(0)
        return idx + 1, out, cur_hidden

    cnt = torch.tensor(0, dtype=torch.int64)
    _, out, final_hidden = while_loop(cond_fn, body_fn, [cnt, step_output, cur_hidden])
    if reverse:
        out = out.flip(0)

    return out, final_hidden.squeeze(0)

