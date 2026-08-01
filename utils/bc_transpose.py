
def bc_transpose(expr):
    collapse = block_collapse(expr.arg)
    return collapse._eval_transpose()

