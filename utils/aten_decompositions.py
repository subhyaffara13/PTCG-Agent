
def aten_decompositions() -> dict[torch._ops.OpOverload, Callable]:
    """Return the ONNX to ATen decomp table."""
    return _impl.ONNX_ATEN_DECOMP_TABLE

