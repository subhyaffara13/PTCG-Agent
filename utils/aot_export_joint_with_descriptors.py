
def aot_export_joint_with_descriptors(
    stack: contextlib.ExitStack,
    mod: nn.Module,
    args: tuple[Any, ...],
    kwargs: dict[str, Any] | None = None,
    *,
    decompositions: dict[OpOverload, Callable[..., Any]] | None = None,
    keep_inference_input_mutations: bool = False,
    ignore_shape_env: bool = False,
    disable_functionalization: bool = False,
    _record_nn_module_stack: bool = False,
    _disable_torch_fn_metadata_mode: bool = False,
) -> JointWithDescriptors:
    """
    This API captures the joint graph for an nn.Module.  However, unlike
    aot_export_joint_simple or aot_export_module(trace_joint=True), the
    calling convention of the produced joint graph follows no fixed positional
    schema; for example, you cannot rely on the second argument of the traced
    joint graph to correspond to the second argument of the module you traced.
    However, the inputs and outputs of the traced graph are schematized
    with **descriptors**, annotated on meta['desc'] on the placeholder and
    return FX nodes, which you can use to determine the meaning of arguments.

    The major benefit of using this export rather than aot_export_joint_simple
    is that we have feature parity with all situations that torch.compile
    supports (via aot_module_simplified), including handling for more
    complicated cases such as multiple differentiable outputs, input mutations
    that must be handled outside of the graph, tensor subclasses, etc.

    What can you do with one of these joint graphs with descriptors?  The
    motivating use case (autoparallel) involves taking the joint graph, doing
    optimizations on it, and then turning it back into a callable so it can be
    torch.compile'd at a later point in time.  This cannot be done as a
    traditional torch.compile joint graph pass for two reasons:

        1. The sharding of parameters must be decided before parameter
           initialization / checkpoint load, far before torch.compile would
           ordinarily run.

        2. We need to change the meaning of parameters (e.g., we might replace
           a replicated parameter with a sharded version of it, changing its
           input size).  torch.compile is ordinarily semantics preserving, and
           not allowed to change the meaning of inputs.

    Some descriptors can be quite exotic, so we recommend thinking carefully
    if there is a safe fallback you can apply to descriptors you don't understand.
    For example, you should have some way to handle not finding a particular
    input exactly as is in the final FX graph inputs.

    Note: When using this API, you must create and enter an ExitStack context
    manager, which will be passed into this function.  This context manager
    must remain active if you call the compile function to finish compilation.
    (TODO: We may relax this requirement by having AOTAutograd keep track of
    how to reconstruct all the context managers at a later point in time.)

    NB: You're not obligated to do a /full/ compile in stage2; instead you can
    leave the forward/backward compilers unspecified in which case the
    partitioned FX graphs will directly run.  The overall autograd Function
    can be allowed in graph so you can reprocess it in the context of a
    (potentially larger) compiled region later.

    NB: These APIs do NOT hit cache, as we only ever cache the final compile results,
    not the intermediate export result.

    NB: If the passed nn.Module has parameters and buffers on it, we will
    generate extra implicit parameter/buffer arguments and assign ParamAOTInput
    and BufferAOTInput descriptors to them.  However, if you generate the input
    nn.Module from a mechanism like Dynamo, you will NOT get these descriptors
    (because Dynamo will already have taken care of lifting the parameters/buffers
    into arguments!)  In that case, it would be necessary to analyze the Sources
    of the inputs to determine if inputs are parameters and their FQNs.
    """

    (
        functional_call,
        _params_buffers_flat,
        params_spec,
        buffers_spec,
        fake_flat_args,
        full_args_descs,
        aot_config,
        fake_mode,
        shape_env,
        in_spec,
        out_spec,
        act_input_indices,
    ) = prepare_aot_module_simplified(
        mod,
        args,
        kwargs,
        # In contrast, decompositions are needed at this stage.
        decompositions,
        keep_inference_input_mutations,
        ignore_shape_env,
        flatten=True,
        # Without this, we will attempt to "compile" the backward lazily
        # at runtime, but this is pointless because it's just boxed_nop,
        # it's trivial.  But this will get Inductor confused about scoping
        # Metric(s) {'is_forward'} have already been set in the current
        # context.
        force_non_lazy_backward_lowering=True,
        disable_functionalization=disable_functionalization,
        _record_nn_module_stack=_record_nn_module_stack,
        _disable_torch_fn_metadata_mode=_disable_torch_fn_metadata_mode,
    )

    # TODO: Maybe this should be in create_aot_state?  Not sure, that would
    # increase its scope
    stack.enter_context(compiled_autograd._disable())

    aot_state = create_aot_state(
        stack,
        functional_call,
        fake_flat_args,
        full_args_descs,
        aot_config,
        fake_mode,
        shape_env,
    )
    aot_state.fw_metadata.act_input_indices = act_input_indices

    # NB: no cache lookup!
    aot_graph_capture = aot_stage1_graph_capture(aot_state, functional_call)

    if out_spec is None or out_spec.spec is None:
        raise AssertionError("out_spec and out_spec.spec must not be None")
    if in_spec is None:
        raise AssertionError("in_spec must not be None")
    return JointWithDescriptors(
        _aot_state=aot_state,
        _aot_graph_capture=aot_graph_capture,
        params_spec=params_spec,
        buffers_spec=buffers_spec,
        in_spec=in_spec,
        out_spec=out_spec.spec,
    )

