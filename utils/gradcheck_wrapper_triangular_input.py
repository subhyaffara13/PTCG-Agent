
def gradcheck_wrapper_triangular_input(op, *args, upper=False, idx=0, **kwargs):
    """Gradcheck wrapper for functions that take lower or upper triangular matrices as input.

    They require a modified function because the finite-difference algorithm
    for calculating derivatives does not preserve the triangular property of the input.
    `idx` is used to specific which `args[idx]` is to be triangularized.
    """
    triangular_arg = args[idx].triu() if upper else args[idx].tril()
    return op(*args[:idx], triangular_arg, *args[idx + 1 :], upper, **kwargs)

