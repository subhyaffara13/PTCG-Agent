
def invoke_subgraph(subgraph_fn: ir.Subgraph, identifier: str, *operands):
    result = ir.InvokeSubgraph.create(subgraph_fn, *operands)
    return list(map(TensorBox.create, result))  # type: ignore[call-overload]


def invoke_subgraph(
    gm: torch.fx.GraphModule, fake_tensor_inputs: list[torch.Tensor], **kwargs: Any
) -> Callable[..., Any]:
    """Backend that wraps forward/backward graphs in invoke_subgraph HOP when traced by make_fx.

    This backend uses AOTAutograd to partition into forward/backward graphs, then wraps
    each in an invoke_subgraph HOP. This is useful for recursive Dynamo tracing scenarios
    where you want the compiled subgraph to appear as invoke_subgraph HOPs in the outer
    trace rather than being inlined.

    Requires:
    - torch._dynamo.config.force_compile_during_fx_trace = True
      (this implicitly overrides error_on_nested_fx_trace)
    """
    if kwargs:
        log.warning("invoke_subgraph backend ignoring extra kwargs %s", kwargs)

    # Use AOTAutograd to partition into forward/backward
    return aot_autograd(
        fw_compiler=invoke_subgraph_inner_compiler,
        bw_compiler=invoke_subgraph_inner_compiler,
        partition_fn=min_cut_rematerialization_partition,
        keep_inference_input_mutations=True,
    )(gm, fake_tensor_inputs)

