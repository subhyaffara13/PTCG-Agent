
def _symeig_backward_complete_eigenspace(D_grad, U_grad, A, D, U):
    # compute F, such that F_ij = (d_j - d_i)^{-1} for i != j, F_ii = 0
    F = D.unsqueeze(-2) - D.unsqueeze(-1)
    F.diagonal(dim1=-2, dim2=-1).fill_(float("inf"))
    F.pow_(-1)

    # A.grad = U (D.grad + (U^T U.grad * F)) U^T
    Ut = U.mT.contiguous()
    res = torch.matmul(
        U, torch.matmul(torch.diag_embed(D_grad) + torch.matmul(Ut, U_grad) * F, Ut)
    )

    return res

