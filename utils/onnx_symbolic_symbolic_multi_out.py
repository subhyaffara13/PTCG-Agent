
def onnx_symbolic_symbolic_multi_out(
    inputs: Sequence[ir.Value | None],
    op_type: str,
    onnx_dtypes: Sequence[int],
    *,
    shapes: Sequence[Sequence[int | ir.Value]],
    attr_keys: Sequence[str],
    attr_types: Sequence[str],
    attr_pos: Sequence[tuple[int, int]],
    attr_ints: Sequence[int],
    attr_floats: Sequence[float],
    attr_strs: Sequence[str],
    metadata_props_keys: Sequence[str] = (),
    metadata_props_values: Sequence[str] = (),
    domain: str = "",
    version: int | None = None,
) -> Sequence[ir.Value]:
    del shapes  # Unused. The shapes are set by the graph builder
    encoded = _symbolic_impl.EncodedAttrs(
        attr_keys=list(attr_keys),
        attr_types=list(attr_types),
        attr_pos=list(attr_pos),
        attr_ints=list(attr_ints),
        attr_floats=list(attr_floats),
        attr_strs=list(attr_strs),
    )
    attrs = encoded.to_dict()
    return _call_symbolic_op(
        op_type,
        domain,
        inputs,
        attrs,
        dtypes=onnx_dtypes,
        version=version,
        metadata_props=dict(zip(metadata_props_keys, metadata_props_values)),
    )

