
def _emit_output_wrapping(
    state: _CodegenState,
    out_metas: list[PlainTensorMeta | SubclassCreationMeta],
) -> tuple[list[str], int]:
    """Emit wrapping code for output metas.

    Returns (result_exprs, num_args_tallied) where result_exprs are Python
    expression strings referencing each wrapped output.
    """
    out_idx_ref = [0]
    result_exprs: list[str] = []
    num_args_tallied = 0

    for meta in out_metas:
        if isinstance(meta, PlainTensorMeta):
            result_exprs.append(f"unwrapped_outs[{meta.unwrapped_idx}]")
            num_args_tallied += 1
            out_idx_ref[0] = max(out_idx_ref[0], meta.unwrapped_idx + 1)
        else:
            result_var = _codegen_wrap_subclass(state, meta, out_idx_ref)
            result_exprs.append(result_var)
            num_args_tallied += meta.arg_count

    return result_exprs, num_args_tallied

