
def trace_hop_function_with_auto_output_flattening(
    f: VariableTracker,
    tx: "InstructionTranslator",
    subtracer: "SubgraphTracer",
    enable_grad: bool | None,
    allow_side_effects: bool,
    args: Sequence[VariableTracker],
    sub_kwargs: dict[str, VariableTracker],
) -> VariableTracker:
    autograd_ctx = (
        dynamo_enable_grad(tx, enable_grad)
        if enable_grad is not None
        else contextlib.nullcontext()
    )
    side_effects_ctx = (
        dynamo_allow_side_effects_in_hop(tx)
        if allow_side_effects
        else contextlib.nullcontext()
    )

    with autograd_ctx, side_effects_ctx:
        output = f.call_function(tx, args, sub_kwargs)

    return output

