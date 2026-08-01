
def aten_gelu_opset20(
    self: TReal,
    approximate: str = "none",
) -> TReal:
    """gelu(Tensor self, *, str approximate="none") -> Tensor"""
    return op20.Gelu(self, approximate=approximate)

