
def _linalg_svd_meta(
    A: Tensor,
    full_matrices: bool = False,
    compute_uv: bool = True,
    driver: str | None = None,
):
    checkIsMatrix(A, "linalg.svd")
    checkFloatingOrComplex(A, "linalg.svd")

    batch_dims = list(A.shape[:-2])
    m = A.shape[-2]
    n = A.shape[-1]
    k = torch.sym_min(m, n)

    if compute_uv:
        U_shape = batch_dims + [m, m if full_matrices else k]
        U = A.new_empty(U_shape)
        U.as_strided_(U_shape, make_contiguous_strides_for(U_shape, row_major=False))

        V_shape = batch_dims + [n if full_matrices else k, n]
        V = A.new_empty(V_shape)
        # NB: This checks for CUDA since there is no way to check for cuSolver.
        # Also, this might not work correctly on CPU when fake_device is not
        # available as device_hint just defaults to CUDA in that case. See
        # _linalg_svd meta in core.
        is_cuda = device_hint(A) == "cuda"
        V.as_strided_(V_shape, make_contiguous_strides_for(V_shape, row_major=is_cuda))
    else:
        # doesn't matter
        U = A.new_empty([0])
        V = A.new_empty([0])

    # S is always real, even when A is complex.
    S = A.new_empty(batch_dims + [k], dtype=toRealValueType(A.dtype))
    return U, S, V

