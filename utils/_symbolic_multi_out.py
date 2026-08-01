
def _symbolic_multi_out(
    inputs: Sequence[torch.Tensor | None],
    op_type: str,
    onnx_dtypes: Sequence[int],
    *,
    shapes: Sequence[Sequence[int | torch.SymInt]],
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
) -> list[torch.Tensor]:
    outputs = []
    torch._check(
        len(shapes) == len(onnx_dtypes),
        lambda: f"Number of shapes ({len(shapes)}) must match number of ONNX dtypes ({len(onnx_dtypes)})",
    )
    for shape, onnx_dtype in zip(shapes, onnx_dtypes):
        torch._check(
            onnx_dtype in _dtype_mappings.ONNX_DTYPE_TO_TORCH_DTYPE,
            lambda: f"{onnx_dtype} is invalid as an ONNX data type. Valid values are {list(_dtype_mappings.ONNX_DTYPE_TO_TORCH_DTYPE.keys())}",
        )
        outputs.append(
            torch.zeros(
                shape, dtype=_dtype_mappings.ONNX_DTYPE_TO_TORCH_DTYPE[onnx_dtype]
            )
        )
    return outputs

