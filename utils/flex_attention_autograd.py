from typing import Any, Callable

def flex_attention_autograd(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    score_mod: Callable,
    block_mask: tuple,
    scale: float,
    kernel_options: dict[str, Any],
    score_mod_other_buffers: tuple[Tensor, ...] = (),
    mask_mod_other_buffers: tuple[Tensor, ...] = (),
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    from torch._dynamo._trace_wrapped_higher_order_op import TransformGetItemToIndex

    with TransformGetItemToIndex():
        input_requires_grad = any(
            isinstance(t, torch.Tensor) and t.requires_grad
            for t in (query, key, value, *score_mod_other_buffers)
        )
        if torch.is_grad_enabled() and input_requires_grad:
            if block_mask[7] is None:
                raise RuntimeError(
                    "BlockMask q_indices is None. Backward pass requires q_indices to be computed. "
                    "Please create the BlockMask with compute_q_blocks=True"
                )
            example_vals = (
                query.new_zeros((), requires_grad=input_requires_grad),
                query.new_zeros((), dtype=torch.int),
                query.new_zeros((), dtype=torch.int),
                query.new_zeros((), dtype=torch.int),
                query.new_zeros((), dtype=torch.int),
            )
            fw_graph, bw_graph = create_fw_bw_graph(
                score_mod, example_vals, score_mod_other_buffers
            )
        else:
            fw_graph, bw_graph = score_mod, None
        out, logsumexp, max_scores = FlexAttentionAutogradOp.apply(
            query,
            key,
            value,
            fw_graph,
            bw_graph,
            block_mask,
            scale,
            kernel_options,
            mask_mod_other_buffers,
            *score_mod_other_buffers,
        )
    return out, logsumexp, max_scores

