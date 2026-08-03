from typing import Any, Callable

def trace_flex_attention_backward(
    proxy_mode: ProxyTorchDispatchMode,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    out: torch.Tensor,
    logsumexp: torch.Tensor,
    grad_out: torch.Tensor,
    grad_logsumexp: torch.Tensor,
    fw_graph: Callable | GraphModule,
    joint_graph: GraphModule,
    block_mask: tuple,
    scale: float,
    kernel_options: dict[str, Any],
    score_mod_other_buffers: tuple = (),
    mask_mod_other_buffers: tuple = (),
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, tuple[torch.Tensor | None, ...]]:
    """We already have the forward graph and joint graph from the forward pass, so we create a proxy attach both graphs"""
    from torch._dynamo._trace_wrapped_higher_order_op import TransformGetItemToIndex

    example_out = flex_attention_backward(
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

    requires_grad = any(pytree.tree_map(lambda x: x.requires_grad, (query, key)))
    fw_example_vals = [query.new_zeros((), requires_grad=requires_grad)] + [
        query.new_zeros((), dtype=torch.int) for _ in range(4)
    ]
    bw_example_vals = fw_example_vals + [query.new_zeros(())]
    mask_example_vals = [query.new_zeros((), dtype=torch.int) for _ in range(4)]
    mask_graph = block_mask[-1]
    with TransformGetItemToIndex():
        # There's no active make_fx during the compiled autograd graph's initial capture
        fw_graph = _maybe_reenter_make_fx(fw_graph)(
            *fw_example_vals, *score_mod_other_buffers
        )
        joint_graph = _maybe_reenter_make_fx(joint_graph)(
            *bw_example_vals, *score_mod_other_buffers
        )
        mask_graph = _maybe_reenter_make_fx(mask_graph)(
            *mask_example_vals, *mask_mod_other_buffers
        )
    if not isinstance(proxy_mode.tracer, torch.fx.Tracer):
        raise AssertionError(
            f"expected proxy_mode.tracer to be torch.fx.Tracer, got {type(proxy_mode.tracer)}"
        )
    block_mask = block_mask[:-1] + (mask_graph,)

    qualname = proxy_mode.tracer.get_fresh_qualname("fw_graph")
    proxy_mode.tracer.root.register_module(qualname, fw_graph)  # type: ignore[arg-type]
    qualname = proxy_mode.tracer.get_fresh_qualname("joint_graph")
    proxy_mode.tracer.root.register_module(qualname, joint_graph)
    qualname = proxy_mode.tracer.get_fresh_qualname("mask_graph")
    proxy_mode.tracer.root.register_module(qualname, mask_graph)

    node_args = (
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
    # pyrefly: ignore [missing-attribute]
    proxy_args = pytree.tree_map(proxy_mode.tracer.unwrap_proxy, node_args)
    out_proxy = proxy_mode.tracer.create_proxy(
        "call_function",
        flex_attention_backward,
        proxy_args,
        {},
        name="flex_attention_backward",
    )
    return track_tensor_tree(
        example_out,
        out_proxy,
        constant=None,
        tracer=proxy_mode.tracer,
    )

