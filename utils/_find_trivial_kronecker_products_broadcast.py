
def _find_trivial_kronecker_products_broadcast(expr: ArrayTensorProduct):
    newargs: list[Basic] = []
    removed = []
    count_dims = 0
    for arg in expr.args:
        count_dims += get_rank(arg)
        shape = get_shape(arg)
        current_range = [count_dims-i for i in range(len(shape), 0, -1)]
        if (shape == (1, 1) and len(newargs) > 0 and 1 not in get_shape(newargs[-1]) and
            isinstance(newargs[-1], MatrixExpr) and isinstance(arg, MatrixExpr)):
            # KroneckerProduct object allows the trick of broadcasting:
            newargs[-1] = KroneckerProduct(newargs[-1], arg)
            removed.extend(current_range)
        elif 1 not in shape and len(newargs) > 0 and get_shape(newargs[-1]) == (1, 1):
            # Broadcast:
            newargs[-1] = KroneckerProduct(newargs[-1], arg)
            prev_range = [i for i in range(min(current_range)) if i not in removed]
            removed.extend(prev_range[-2:])
        else:
            newargs.append(arg)
    return _array_tensor_product(*newargs), removed

