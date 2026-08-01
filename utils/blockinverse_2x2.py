
def blockinverse_2x2(expr):
    if isinstance(expr.arg, BlockMatrix) and expr.arg.blockshape == (2, 2):
        # See: Inverses of 2x2 Block Matrices, Tzon-Tzer Lu and Sheng-Hua Shiou
        [[A, B],
         [C, D]] = expr.arg.blocks.tolist()

        formula = _choose_2x2_inversion_formula(A, B, C, D)
        if formula != None:
            MI = expr.arg.schur(formula).I
        if formula == 'A':
            AI = A.I
            return BlockMatrix([[AI + AI * B * MI * C * AI, -AI * B * MI], [-MI * C * AI, MI]])
        if formula == 'B':
            BI = B.I
            return BlockMatrix([[-MI * D * BI, MI], [BI + BI * A * MI * D * BI, -BI * A * MI]])
        if formula == 'C':
            CI = C.I
            return BlockMatrix([[-CI * D * MI, CI + CI * D * MI * A * CI], [MI, -MI * A * CI]])
        if formula == 'D':
            DI = D.I
            return BlockMatrix([[MI, -MI * B * DI], [-DI * C * MI, DI + DI * C * MI * B * DI]])

    return expr

