
def transpose_matmul(
    A: torch.Tensor, B: torch.Tensor, Atrans: bool, Btrans: bool
) -> torch.Tensor:
    if Atrans:
        A = A.transpose(-1, -2)
    if Btrans:
        B = B.transpose(-1, -2)
    return torch.matmul(A, B)

