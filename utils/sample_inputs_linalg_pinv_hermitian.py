
def sample_inputs_linalg_pinv_hermitian(
    op_info, device, dtype, requires_grad=False, **kwargs
):
    """
    This function generates input for torch.linalg.pinv with hermitian=True keyword argument.
    """
    for o in sample_inputs_linalg_invertible(
        op_info, device, dtype, requires_grad, **kwargs
    ):
        o.kwargs = {"hermitian": True}
        yield o

