
def construct_tensor_variable(
    target_cls: type[VTTypeAlias],
    tx: "InstructionTranslatorBase",
    proxy: torch.fx.Proxy,
    example_value: Any,
    subclass_type: type | None,
    options: dict[str, Any],
) -> VTTypeAlias:
    """
    Actually construct a tensor variable after all the pre-processing from
    wrapping a pre-existing or newly created tensor value.
    """
    # NB: In most (all?) cases, this does not actually do a clone.
    # (WARNING: this means that if we mutate metadata on the fake
    # tensor, the stored example value will update too!)
    example_value = _clone_input(example_value, tx.fake_mode)
    set_example_value(proxy.node, example_value)
    # We bind the unbacked symints in sizes/trdies of tensor lazily.
    # So that subgraphs can access the unbacked symbol's proxy in parent graph
    # when lifting unbacked symbols of input tensors to subgraph inputs.
    # We do it lazily because the tensor may not be used in subgraphs.
    if proxy.node.op != "placeholder":
        tx.output.current_tracer.track_produced_symints(example_value, proxy)
    options.update(get_specialized_props(target_cls, tx, example_value, subclass_type))
    # pyrefly: ignore [bad-argument-count]
    return target_cls(proxy, **options)

