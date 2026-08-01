
def codegen_subclass_wrapper(
    compiled_fn: Callable[..., object],
    inp_metas: list[PlainTensorMeta | SubclassCreationMeta],
    out_metas: list[PlainTensorMeta | SubclassCreationMeta],
    num_fw_outs_saved_for_bw: int | None,
    frozen_inp_indices: frozenset[int] = frozenset(),
    act_input_indices: list[int] | None = None,
) -> Callable[..., object]:
    """Generate a specialized wrapper function for subclass unwrap/wrap."""
    source, globals_dict = _codegen_subclass_wrapper_source(
        inp_metas,
        out_metas,
        num_fw_outs_saved_for_bw,
        frozen_inp_indices,
        act_input_indices=act_input_indices,
    )
    globals_dict["compiled_fn"] = compiled_fn
    return _compile_and_exec_source(
        source, globals_dict, "inner_fn", "subclass_wrapper", wrapped_fn=compiled_fn
    )

