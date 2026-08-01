
def _symbolic(
    inputs: Sequence[torch.Tensor | None],
    op_type: str,
    onnx_dtype: int,
    *,
    shape: Sequence[int | torch.SymInt],
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
) -> torch.Tensor:
    torch._check(
        onnx_dtype in _dtype_mappings.ONNX_DTYPE_TO_TORCH_DTYPE,
        lambda: f"{onnx_dtype} is invalid as an ONNX data type. Valid values are {list(_dtype_mappings.ONNX_DTYPE_TO_TORCH_DTYPE.keys())}",
    )
    return torch.zeros(
        shape, dtype=_dtype_mappings.ONNX_DTYPE_TO_TORCH_DTYPE[onnx_dtype]
    )

