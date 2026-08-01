
def trace_flex_attention(
    proxy_mode: ProxyTorchDispatchMode,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    score_mod: Callable,
    block_mask: tuple,
    scale: float,
    kernel_options: dict[str, Any],
    score_mod_other_buffers: tuple = (),
    mask_mod_other_buffers: tuple = (),
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Traces the flex_attention operator with the given score_mod function and other_buffers.

    Trace SDPA will call make_fx with "fake" example vals and then trace the score_mod function
    This will produce a GraphModule that will be stored on the root tracer as "sdpa_score". We
    access this graph module in inductor to inline the score_mod function to the triton template.
    """
    from torch._dynamo._trace_wrapped_higher_order_op import TransformGetItemToIndex

    example_out = flex_attention(
        query,
        key,
        value,
        score_mod,
        block_mask,
        scale,
        kernel_options,
        score_mod_other_buffers,
        mask_mod_other_buffers,
    )
    example_vals = [query.new_zeros((), requires_grad=query.requires_grad)] + [
        query.new_zeros((), dtype=torch.int) for _ in range(4)
    ]
    mask_example_vals = [query.new_zeros((), dtype=torch.int) for _ in range(4)]
    mask_mod = block_mask[-1]
    with TransformGetItemToIndex():
        score_graph = reenter_make_fx(score_mod)(
            *example_vals, *score_mod_other_buffers
        )
        mask_graph = reenter_make_fx(mask_mod)(
            *mask_example_vals, *mask_mod_other_buffers
        )
    if not isinstance(proxy_mode.tracer, torch.fx.Tracer):
        raise AssertionError(
            f"expected proxy_mode.tracer to be torch.fx.Tracer, got {type(proxy_mode.tracer)}"
        )
    block_mask = block_mask[:-1] + (mask_graph,)
    qualname = proxy_mode.tracer.get_fresh_qualname("sdpa_score")
    proxy_mode.tracer.root.register_module(qualname, score_graph)
    mask_qualname = proxy_mode.tracer.get_fresh_qualname("sdpa_mask")
    proxy_mode.tracer.root.register_module(mask_qualname, mask_graph)
    node_args = (
        query,
        key,
        value,
        score_graph,
        block_mask,
        scale,
        kernel_options,
        score_mod_other_buffers,
        mask_mod_other_buffers,
    )
    # pyrefly: ignore [missing-attribute]
    proxy_args = pytree.tree_map(proxy_mode.tracer.unwrap_proxy, node_args)
    with torch.fx.experimental.proxy_tensor.set_original_aten_op(flex_attention):
        out_proxy = proxy_mode.tracer.create_proxy(
            "call_function", flex_attention, proxy_args, {}
        )
    return track_tensor_tree(
        example_out,
        out_proxy,
        constant=None,
        tracer=proxy_mode.tracer,
    )

