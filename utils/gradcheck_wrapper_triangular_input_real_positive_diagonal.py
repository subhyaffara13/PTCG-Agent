
def gradcheck_wrapper_triangular_input_real_positive_diagonal(
    op, *args, upper=False, idx=0, **kwargs
):
    """Gradcheck wrapper for functions that take lower/upper triangular matrices
    with real and positive diagonals, for example, cholesky-like operations.
    """
    arg = args[idx]
    arg_diag = arg.diagonal(0, -2, -1)
    arg_diag_embed = torch.diag_embed(arg_diag)
    id_diag_tensor = torch.ones_like(arg_diag)
    id_tensor = torch.diag_embed(id_diag_tensor)
    # new_arg = arg - diag(arg) + I
    new_arg = arg - arg_diag_embed + id_tensor
    return gradcheck_wrapper_triangular_input(
        op, *args[:idx], new_arg, *args[idx + 1 :], upper=upper, idx=idx, **kwargs
    )

