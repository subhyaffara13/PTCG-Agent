
def linalg_lu_solve_out_mps(LU, pivots, B, *, left=True, adjoint=False, out):
    if out.numel() == 0:
        return

    if not left:
        adjoint = not adjoint
        B = B.mH

    if adjoint:
        lu_ = LU.mH
        x = torch.linalg.solve_triangular(lu_, B, left=True, upper=False)
        x = torch.linalg.solve_triangular(
            lu_, x, left=True, upper=True, unitriangular=True
        )
        x = _apply_pivots(x, pivots, LU.shape[:-1], inverse=True)
    else:
        x = _apply_pivots(B, pivots, LU.shape[:-1])
        x = torch.linalg.solve_triangular(
            LU, x, left=True, upper=False, unitriangular=True
        )
        x = torch.linalg.solve_triangular(LU, x, left=True, upper=True)

    if not left:
        x = x.mH

    out.copy_(x)

