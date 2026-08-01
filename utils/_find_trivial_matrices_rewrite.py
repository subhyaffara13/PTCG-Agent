
def _find_trivial_matrices_rewrite(expr: ArrayTensorProduct):
    # If there are matrices of trivial shape in the tensor product (i.e. shape
    # (1, 1)), try to check if there is a suitable non-trivial MatMul where the
    # expression can be inserted.

    # For example, if "a" has shape (1, 1) and "b" has shape (k, 1), the
    # expressions "_array_tensor_product(a, b*b.T)" can be rewritten as
    # "b*a*b.T"

    trivial_matrices = []
    pos: int | None = None  # must be initialized else causes UnboundLocalError
    first: MatrixExpr | None = None  # may cause UnboundLocalError if not initialized
    second: MatrixExpr | None = None  # may cause UnboundLocalError if not initialized
    removed: list[int] = []
    counter: int = 0
    args: list[Basic | None] = list(expr.args)
    for i, arg in enumerate(expr.args):
        if isinstance(arg, MatrixExpr):
            if arg.shape == (1, 1):
                trivial_matrices.append(arg)
                args[i] = None
                removed.extend([counter, counter+1])
            elif pos is None and isinstance(arg, MatMul):
                margs = arg.args
                for j, e in enumerate(margs):
                    if isinstance(e, MatrixExpr) and e.shape[1] == 1:
                        pos = i
                        first = MatMul.fromiter(margs[:j+1])
                        second = MatMul.fromiter(margs[j+1:])
                        break
        counter += get_rank(arg)
    if pos is None:
        return expr, []
    args[pos] = (first*MatMul.fromiter(i for i in trivial_matrices)*second).doit()
    return _array_tensor_product(*[i for i in args if i is not None]), removed

