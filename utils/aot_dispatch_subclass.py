from typing import Any, Callable

def aot_dispatch_subclass(
    flat_fn_maybe_joint: JointTraceFn | TraceFn,
    args: list[FxValue] | tuple[list[FxValue], list[FxValue]],
    args_descs: list[AOTInput] | tuple[list[AOTInput], list[AOTInput]],
    *,
    is_joint_structure: bool,
    meta: ViewAndMutationMeta,
    fw_only: Callable[..., Any],
) -> SubclassTracingInfo:
    # Skip logic if we don't need to trace through any subclasses
    req_subclass_dispatch = requires_subclass_dispatch(args, meta)  # type: ignore[arg-type]
    if not req_subclass_dispatch:
        return SubclassTracingInfo(
            plain_tensor_trace_fn=flat_fn_maybe_joint,
            plain_tensor_args=args,
            plain_tensor_args_descs=args_descs,
            maybe_subclass_meta=None,
        )

    # TODO: add subclass guards (later PR).

    # What's going on here? We need to compute subclass metadata about the outputs of the joint (grad_inputs).
    # Annoying: we don't know the grad input metas until we're in the middle of tracing the joint,
    # so we set it later, while we're tracing the joint (see inner_fn() below).
    # Another option would be to run our run_functionalized_fw_and_collect_metadata() function
    # directly on the joint, but this would hurt compile time (adding yet another pass through the joint).
    subclass_meta = SubclassMeta()

    # NB: doesn't take descs, this is going from the NEW flat_args to the
    # subclasses, we don't need to do bookkeeping here
    def inner_fn(fn: Callable[..., Any], args: Any, *, use_trace_joint: bool) -> Any:
        # Step 1: wrap tensor inputs into subclasses if necessary
        all_args = wrap_tensor_subclasses_maybe_joint(
            args, is_joint_structure=use_trace_joint, meta=meta
        )

        # Step 2: call the inner function, with our (maybe subclass) inputs
        wrapped_outs, wrapped_outs_descs = call_and_expect_output_descs(fn, all_args)  # type: ignore[arg-type]

        if use_trace_joint:
            # See Note: [Computing Subclass Metadata about grad_inputs]
            # We also stash subclass info on our grad_inputs, if we're tracing the joint.
            nonlocal subclass_meta
            if not (isinstance(wrapped_outs, tuple) and len(wrapped_outs) == 2):
                raise AssertionError(
                    f"expected wrapped_outs to be tuple of length 2, got {type(wrapped_outs)}, {wrapped_outs_descs}"
                )
            # Don't need fw outs since we already have subclass metadata on them
            grad_inputs = wrapped_outs[1]
            subclass_meta.grad_input_metas = create_subclass_meta(grad_inputs)

            # Add extra symints as outputs to the forward/backward graphs
            # ignore nested ints here
            forward_outs, forward_outs_descs = unwrap_tensor_subclasses(
                wrapped_outs[0],
                wrapped_outs_descs[0],
                append_symints=True,
            )
            # ignore nested ints here
            backward_outs, backward_outs_descs = unwrap_tensor_subclasses(
                wrapped_outs[1],
                wrapped_outs_descs[1],
                append_symints=True,
            )
            return (
                (forward_outs, backward_outs),
                (forward_outs_descs, backward_outs_descs),
            )

        # Step 3: Unwrap any subclass outputs back into dense tensors
        return unwrap_tensor_subclasses(
            wrapped_outs, wrapped_outs_descs, append_symints=True
        )

    def joint_fn(
        primals: list[FxValue], tangents: list[FxValue]
    ) -> tuple[
        tuple[list[FxValue], list[FxValue]], tuple[list[AOTOutput], list[AOTOutput]]
    ]:
        with maybe_enable_thunkify():
            return inner_fn(
                flat_fn_maybe_joint, (primals, tangents), use_trace_joint=True
            )

    def fw_fn(*primals: FxValue) -> tuple[list[FxValue], list[AOTOutput]]:
        with maybe_enable_thunkify():
            return inner_fn(flat_fn_maybe_joint, primals, use_trace_joint=False)

    def metadata_fn(*primals: FxValue) -> tuple[list[FxValue], list[AOTOutput]]:
        @simple_wraps(fw_only)
        def inner_fw_only(*args: Any) -> Any:
            return call_and_expect_output_descs(fw_only, args)

        return inner_fn(inner_fw_only, primals, use_trace_joint=False)

    if is_joint_structure:
        primals_wrapped: list[FxValue] = typing.cast(list[FxValue], args[0])
        primals_wrapped_descs: list[AOTInput] = typing.cast(
            list[AOTInput], args_descs[0]
        )
        tangents_wrapped: list[FxValue] = typing.cast(list[FxValue], args[1])
        tangents_wrapped_descs: list[AOTInput] = typing.cast(
            list[AOTInput], args_descs[1]
        )

        # Add extra symints (size/strides) as input to the forward graph
        primals_unwrapped_pair = unwrap_tensor_subclasses(
            primals_wrapped,
            primals_wrapped_descs,
            append_symints=True,
        )
        # We pass append_symints=False here because the partitioner will
        # capture and add any extra argument.
        tangents_unwrapped_pair = unwrap_tensor_subclasses(
            tangents_wrapped,
            tangents_wrapped_descs,
            append_symints=False,
        )

        args_unwrapped = (primals_unwrapped_pair[0], tangents_unwrapped_pair[0])
        args_descs_unwrapped = (primals_unwrapped_pair[1], tangents_unwrapped_pair[1])
        remapped_static_indices = remap_unwrapped_subclass_arg_indices(
            primals_wrapped,
            meta.static_input_indices,  # type: ignore[arg-type]
        )

        primals_unwrapped = args_unwrapped[0]  # type: ignore[assignment]
        primals_unwrapped_descs = args_descs_unwrapped[0]  # type: ignore[assignment]
        fn_to_trace = joint_fn  # type: ignore[assignment]
    else:
        primals_wrapped: list[FxValue] = typing.cast(list[FxValue], args)
        primals_wrapped_descs: list[AOTInput] = typing.cast(list[AOTInput], args_descs)

        args_unwrapped, args_descs_unwrapped = unwrap_tensor_subclasses(  # type: ignore[assignment]
            primals_wrapped,
            primals_wrapped_descs,
            append_symints=True,
        )
        remapped_static_indices = remap_unwrapped_subclass_arg_indices(
            primals_wrapped,
            meta.static_input_indices,  # type: ignore[arg-type]
        )

        primals_unwrapped = args_unwrapped  # type: ignore[assignment]
        primals_unwrapped_descs = args_descs_unwrapped  # type: ignore[assignment]
        fn_to_trace = fw_fn  # type: ignore[assignment]

    # Note: [Partitioner handling for Subclasses, Part 1]
    # The way the partitioner works is that:
    # (1) we pass is a single graph containing the joint fw/bw,
    #     where the # of graph outputs corresponds to # fw_outputs + # grad_inputs
    # (2) The partitioner accepts an arguments, num_fwd_outputs,
    #     and assumes that the first "num_fwd_outputs" graph outputs correspond
    #     to outputs of the forward graph.
    # How do tensor subclasses enter the picture?
    # the num_fwd_outputs in the final graph is actually non-trivial to compute,
    # because it can be influenced by input mutations and intermediate bases.
    # So we compute it by inspecting the current ViewAndMutationMeta object.
    # However, the original ViewAndMutationMeta that we computed was created
    # on the subclass -> subclass graph,
    # which can have a different number of outputs than the dense -> dense graph.
    # That's why we created a fresh metadata object on the dense -> dense function here,
    # and plumb it back up to the partitioner.
    # See Note: [Partitioner handling for Subclasses, Part 2] for more info.
    meta_updated = run_functionalized_fw_and_collect_metadata(
        without_output_descs(metadata_fn),
        # pyrefly: ignore [bad-argument-type]
        flat_args_descs=primals_unwrapped_descs,
        static_input_indices=remapped_static_indices,
        keep_input_mutations=meta.keep_input_mutations,
        # pyrefly: ignore [not-iterable]
    )(*primals_unwrapped)

    subclass_meta.fw_metadata = meta_updated

    return SubclassTracingInfo(
        plain_tensor_trace_fn=fn_to_trace,
        plain_tensor_args=args_unwrapped,
        plain_tensor_args_descs=args_descs_unwrapped,
        maybe_subclass_meta=subclass_meta,
    )

