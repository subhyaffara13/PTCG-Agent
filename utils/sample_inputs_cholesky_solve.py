
def sample_inputs_cholesky_solve(op_info, device, dtype, requires_grad=False, **kwargs):
    cholesky_inverse_samples = sample_inputs_linalg_cholesky_inverse(
        op_info, device, dtype, requires_grad=False
    )

    for sample in cholesky_inverse_samples:
        psd_matrix = sample.input
        sample.input = make_tensor(psd_matrix.shape, dtype=dtype, device=device, requires_grad=requires_grad, low=None, high=None)
        sample.args = (psd_matrix.requires_grad_(requires_grad),)
        yield sample

