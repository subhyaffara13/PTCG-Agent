
def _linalg_matrix_norm(
    g: jit_utils.GraphContext,
    self: torch._C.Value,
    ord: torch._C.Value,
    dim: list[int],
    keepdim: bool,
    dtype: torch._C.Value,
):
    return opset9.linalg_matrix_norm(g, self, ord, dim, keepdim, dtype)

