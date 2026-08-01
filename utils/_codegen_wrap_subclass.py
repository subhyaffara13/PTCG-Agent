
def _codegen_wrap_subclass(
    state: _CodegenState,
    meta: SubclassCreationMeta,
    out_idx_ref: list[int],
) -> str:
    """Emit code to reconstruct one subclass output. Returns the variable name."""
    inner_dict_var = state.fresh_name("_out_inner")
    entries: list[str] = []

    for attr, attr_meta in meta.attrs.items():
        match attr_meta:
            case PlainTensorMeta() | OpaqueMeta():
                idx = out_idx_ref[0]
                out_idx_ref[0] += 1
                entries.append(f"{attr!r}: unwrapped_outs[{idx}]")
            case SubclassCreationMeta():
                nested_var = _codegen_wrap_subclass(state, attr_meta, out_idx_ref)
                entries.append(f"{attr!r}: {nested_var}")

    state.emit(f"{inner_dict_var} = {{{', '.join(entries)}}}")

    # Reconstruct outer_size and outer_stride
    size_placeholders = _compute_placeholders(meta.outer_size)
    stride_placeholders = _compute_placeholders(meta.outer_stride)

    def _build_tuple(
        outer: Iterable[None | int | SymInt], placeholders: list[bool]
    ) -> str:
        parts: list[str] = []
        for val, is_sym in zip(outer, placeholders):
            if is_sym:
                idx = out_idx_ref[0]
                out_idx_ref[0] += 1
                parts.append(f"unwrapped_outs[{idx}]")
            else:
                parts.append(repr(_concrete_value(val)))
        if len(parts) == 1:
            return f"({parts[0]},)"
        return f"({', '.join(parts)})"

    size_expr = _build_tuple(meta.outer_size, size_placeholders)
    stride_expr = _build_tuple(meta.outer_stride, stride_placeholders)

    type_name = state.add_global(
        state.fresh_name("_subclass_type"),
        meta.original_subclass_type or type(meta.original_subclass),
    )
    meta_name = state.add_global(state.fresh_name("_meta"), meta.meta)

    result_var = state.fresh_name("_out")
    state.emit(
        f"{result_var} = {type_name}.__tensor_unflatten__("
        f"{inner_dict_var}, {meta_name}, {size_expr}, {stride_expr})"
    )
    return result_var

