
def _thnn_fused_lstm_cell_meta(
    input_gates,
    hidden_gates,
    cx,
    input_bias=None,
    hidden_bias=None,
):
    rnn_cell_checkSizes(input_gates, hidden_gates, input_bias, hidden_bias, 4, cx)
    workspace = torch.empty_like(input_gates, memory_format=torch.contiguous_format)
    hy = torch.empty_like(cx, memory_format=torch.contiguous_format)
    cy = torch.empty_like(cx, memory_format=torch.contiguous_format)
    return (hy, cy, workspace)

