
def trace_hop_function(
    f: VariableTracker,
    tx: "InstructionTranslator",
    subtracer: "SubgraphTracer",
    enable_grad: bool | None,
    restore_side_effects: bool,
    args: Sequence[VariableTracker],
    sub_kwargs: dict[str, VariableTracker],
) -> VariableTracker:
    # For autograd.Function and other legacy HOPs, we do NOT couple
    # restore_side_effects with allow_side_effects_in_hop.
    # This preserves the old behavior where:
    # - restore_side_effects=False means ctx mutations persist
    # - But non-ctx side effects still cause graph breaks (under_activation_checkpoint was False)
    enable_side_effects_with_extra_outputs = False

    autograd_ctx = (
        dynamo_enable_grad(tx, enable_grad)
        if enable_grad is not None
        else contextlib.nullcontext()
    )
    side_effects_ctx = (
        dynamo_allow_side_effects_in_hop(tx)
        if enable_side_effects_with_extra_outputs
        else contextlib.nullcontext()
    )

    # For handling side effects, we can make an argument that we don't
    # have to do anything here. The side effects infra does a good job
    # of graph breaking if we mutate any nonlocal or global variable
    # while subtracing. As a result if tracing succeeds, side effects
    # data structure will only contain read-only data structures that
    # are put there for tracking purposes.
    # But on the other hand, there is an argument that if we ever write
    # a new side effect in Dynamo which does not go through the side
    # effect infra, we can end up in bad state.
    # Therefore we restore the side effects after tracing. The catch is
    # that we have to special handle tensor variables. If we have seen a
    # nonlocal variable tensor during subtracing, we want to keep a
    # track of that tensor, so that later subtracing or the root tracer
    # itself does not create a new proxy for the already observed tensor
    # variable.
    prev_side_effects = None
    if restore_side_effects:
        prev_side_effects = tx.output.side_effects.clone()

    with autograd_ctx, side_effects_ctx:
        output = f.call_function(tx, args, sub_kwargs)

    if restore_side_effects:
        new_side_effects = tx.output.side_effects.clone()
        assert prev_side_effects is not None
        prev_side_effects.track_runahead_tensor_and_symvar_side_effects(
            new_side_effects
        )
        tx.output.side_effects = prev_side_effects
    return output

