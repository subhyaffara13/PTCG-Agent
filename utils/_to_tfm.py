
def _to_TFM(mat, var):
    """Private method to convert ImmutableMatrix to TransferFunctionMatrix efficiently"""
    to_tf = lambda expr: TransferFunction.from_rational_expression(expr, var)
    arg = [[to_tf(expr) for expr in row] for row in mat.tolist()]
    return TransferFunctionMatrix(arg)

