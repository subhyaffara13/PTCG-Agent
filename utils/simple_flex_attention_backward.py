
def simple_flex_attention_backward(
    query,
    key,
    value,
    out,
    logsumexp,
    grad_out,
    grad_logsumexp,
    fw_graph,
    joint_graph,
    block_mask,
    scale,
    kernel_options,
    score_mod_other_buffers,
    mask_mod_other_buffers,
):
    return torch.ops.higher_order.flex_attention_backward(
        query,
        key,
        value,
        out,
        logsumexp,
        grad_out,
        grad_logsumexp,
        fw_graph,
        joint_graph,
        block_mask,
        scale,
        kernel_options,
        score_mod_other_buffers,
        mask_mod_other_buffers,
    )

