
def _codegen_subclass_wrapper_source(
    inp_metas: list[PlainTensorMeta | SubclassCreationMeta],
    out_metas: list[PlainTensorMeta | SubclassCreationMeta],
    num_fw_outs_saved_for_bw: int | None,
    frozen_inp_indices: frozenset[int] = frozenset(),
    act_input_indices: list[int] | None = None,
) -> tuple[str, dict[str, object]]:
    """Generate source and globals for a subclass wrapper.

    Returns (source, globals_dict).  The globals_dict will NOT contain
    ``compiled_fn`` — the caller is responsible for adding it before exec.
    """
    state = _CodegenState()

    state.emit("def inner_fn(args):", indent=0)

    # --- Resolve AsyncCollectiveTensors ---
    # ACTs are transient eager-mode wrappers for async collective overlap.
    # Inductor triton kernels bypass __torch_dispatch__, so we must call
    # trigger_wait() before the compiled graph uses the data.
    if act_input_indices:
        for i in act_input_indices:
            state.emit(f"args[{i}] = args[{i}].trigger_wait()")

    # --- Input unwrapping ---
    state.emit("unwrapped_args = []")
    _emit_input_unwrapping(state, inp_metas, frozen_inp_indices=frozen_inp_indices)

    # Pass through any trailing args not covered by inp_metas
    # (e.g. rng seed/offset added by FunctionalizedRngRuntimeWrapper).
    num_inp_metas = len(inp_metas)
    state.emit(f"unwrapped_args.extend(args[{num_inp_metas}:])")
    state.emit("args.clear()")

    # --- Call compiled function ---
    state.emit("unwrapped_outs = compiled_fn(unwrapped_args)")

    # --- Output wrapping ---
    result_exprs, num_args_tallied = _emit_output_wrapping(state, out_metas)
    result_tuple = f"({', '.join(result_exprs)},)" if result_exprs else "()"
    if num_fw_outs_saved_for_bw is not None:
        state.emit(
            f"return {result_tuple} + tuple(unwrapped_outs[{num_args_tallied}:])"
        )
    else:
        state.emit(f"return {result_tuple}")

    source = "\n".join(state.lines)
    return source, state.globals

