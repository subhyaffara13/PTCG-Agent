
def sample_inputs_svd_lowrank(op_info, device, dtype, requires_grad=False, **kwargs):
    # Function that's well defined on the outputs for complex inputs
    def fn(usv):
        U, S, V = usv
        return U @ V.mH, S

    for (a, b) in sample_inputs_singular_matrix_factors(op_info, device, dtype, requires_grad):
        *batch, m, k = a.shape
        n = b.shape[-2]

        # NOTE: since svd_lowrank relies on non rank-revealing SVD,
        # it inherits the problem of unstable behavior with repeated
        # singular values including zeros.
        # Since we want to avoid (repeated) zeros as singular values,
        # we can only use k for q.
        # This issues could be resolved with using a rank-revealing SVD
        # which does not include "zero" singular values.
        yield SampleInput(a, b, q=k, M=None).with_metadata(output_process_fn_grad=fn)

    for (a, b) in sample_inputs_singular_matrix_factors(op_info, device, dtype, requires_grad):
        *batch, m, k = a.shape
        n = b.shape[-2]
        M = make_tensor((*batch, m, n), dtype=dtype, device=device, requires_grad=requires_grad)
        yield SampleInput(a, b, q=k, M=M).with_metadata(output_process_fn_grad=fn)

