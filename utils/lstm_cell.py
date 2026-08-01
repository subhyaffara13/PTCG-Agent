
def lstm_cell(inp, hx, cx, hh_weight, hh_bias, hr_weight, chunk_dim):
    gates = F.linear(hx, hh_weight, hh_bias) + inp
    chunked_gates = gates.chunk(4, chunk_dim)
    in_gate = chunked_gates[0].sigmoid()
    forget_gate = chunked_gates[1].sigmoid()
    cell_gate = chunked_gates[2].tanh()
    out_gate = chunked_gates[3].sigmoid()
    cy = forget_gate * cx + (in_gate * cell_gate)
    hy = out_gate * cy.tanh()
    hy = hy if hr_weight is None else F.linear(hy, hr_weight, None)

    return hy, cy


def lstm_cell(g: jit_utils.GraphContext, self, hidden, w_ih, w_hh, b_ih, b_hh):
    input = symbolic_helper._unsqueeze_helper(g, self, [0])
    hidden = symbolic_helper._unpack_list(hidden)
    hidden = [symbolic_helper._unsqueeze_helper(g, x, [0]) for x in hidden]
    weight = (
        (w_ih, w_hh, b_ih, b_hh) if symbolic_helper._is_tensor(b_ih) else (w_ih, w_hh)
    )
    has_biases = bool(symbolic_helper._is_tensor(b_ih))
    _, h_outs, c_outs = _generic_rnn(
        g,
        "LSTM",
        input,
        hidden,
        weight,
        has_biases,
        num_layers=1,
        dropout=0,
        train=0,
        bidirectional=False,
        batch_first=False,
    )
    return symbolic_helper._squeeze_helper(
        g, h_outs, [0]
    ), symbolic_helper._squeeze_helper(g, c_outs, [0])

