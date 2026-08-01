
def one_layer_rnn(inp, hidden, params, has_biases, hidden_fn, reverse=False):
    ih_weight = params[0]
    hh_weight = params[1]
    ih_bias = params[2] if has_biases else None
    hh_bias = params[3] if has_biases else None

    precomputed_input = F.linear(inp, ih_weight, ih_bias)
    precomputed_input = precomputed_input.flip(0) if reverse else precomputed_input
    cur_hidden = hidden.unsqueeze(0)
    step_output = []
    for i in precomputed_input:
        cur_hidden = hidden_fn(i, cur_hidden, ih_weight, ih_bias, hh_weight, hh_bias)
        step_output.append(cur_hidden)

    if reverse:
        step_output.reverse()

    out = torch.cat(step_output, 0)

    return out, cur_hidden.squeeze(0)

