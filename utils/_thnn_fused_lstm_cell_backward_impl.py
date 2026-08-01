
def _thnn_fused_lstm_cell_backward_impl(grad_hy, grad_cy, cx, cy, workspace, has_bias):
    if grad_hy is None and grad_cy is None:
        return None, None, None
    checkLSTMBackwardSizes(grad_hy, grad_cy, cx, cy, workspace)
    grad_gates = torch.empty_like(
        workspace, memory_format=legacy_contiguous_memory_format
    )
    grad_cx = torch.empty_like(cx, memory_format=legacy_contiguous_memory_format)
    grad_bias = grad_gates.sum(0, keepdim=False) if has_bias else None
    return grad_gates, grad_cx, grad_bias

