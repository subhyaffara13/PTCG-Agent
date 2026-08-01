
def build_stmts(ctx, stmts):
    stmts = [build_stmt(ctx, s) for s in stmts]
    return list(filter(None, stmts))

