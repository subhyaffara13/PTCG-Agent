
def add_call_function(
    tx: "InstructionTranslator",
    fn: Any,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    flat_example_value: Any,
    config: NestedCompileRegionOptions | None = None,
) -> VariableTracker:
    from .builder import wrap_fx_proxy

    proxy = tx.output.create_proxy(
        "call_function",
        fn,
        args=args,
        kwargs=kwargs,
    )

    # Set backend metadata if provided
    if config is not None:
        if "custom" not in proxy.node.meta:
            # pyrefly: ignore [implicit-any]
            proxy.node.meta["custom"] = {}
        proxy.node.meta["custom"]["nested_region_config"] = config
        assert proxy.node.target == torch._higher_order_ops.invoke_subgraph

    # Store the invocation as a call
    flat_variable = wrap_fx_proxy(
        tx=tx,
        proxy=proxy,
        example_value=flat_example_value,
    )
    return flat_variable

