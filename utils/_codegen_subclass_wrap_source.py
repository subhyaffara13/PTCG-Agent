
def _codegen_subclass_wrap_source(
    out_metas: list[PlainTensorMeta | SubclassCreationMeta],
) -> tuple[str, dict[str, object]]:
    """Generate source for wrapping flat outputs into subclasses.

    Used for the backward epilogue. Shares output-wrapping logic with
    _codegen_subclass_wrapper_source via _emit_output_wrapping.
    """
    state = _CodegenState()
    state.emit("def wrap_fn(unwrapped_outs):", indent=0)
    result_exprs, _ = _emit_output_wrapping(state, out_metas)
    result_tuple = f"({', '.join(result_exprs)},)" if result_exprs else "()"
    state.emit(f"return {result_tuple}")
    source = "\n".join(state.lines)
    return source, state.globals

