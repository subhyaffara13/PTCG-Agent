
def _addmm_activation(
    self: Tensor,
    mat1: Tensor,
    mat2: Tensor,
    beta: int = 1,
    alpha: int = 1,
    use_gelu: bool = False,
):
    out = addmm(self, mat1, mat2, beta, alpha)
    if use_gelu:
        if self.is_cuda:
            return aten.gelu(out, approximate="tanh")
        else:
            return aten.gelu(out)
    return aten.relu(out)

