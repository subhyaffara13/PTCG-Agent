
def addmv(self: Tensor, mat1: Tensor, vec: Tensor, beta: int = 1, alpha: int = 1):
    if not self.is_floating_point() and not self.is_complex():
        beta = int(beta)
        alpha = int(alpha)
    out = alpha * torch.mv(mat1, vec)
    if beta == 0:
        return out
    if out.numel() == 0:  # handle empty matrix
        return beta * self
    return out + beta * self

