
def _svd_meta(
    A: TensorLikeType, *, full_matrices: bool
) -> tuple[TensorLikeType, TensorLikeType, TensorLikeType]:
    utils.check_is_matrix(A, "linalg.svd")
    utils.check_fp_or_complex(A.dtype, "linalg.svd", allow_low_precision_dtypes=False)

    A_shape = A.shape
    batch = A_shape[:-2]
    m, n = A_shape[-2:]
    k = min(m, n)

    shape_U = batch + (m, m if full_matrices else k)
    strides_U = utils.make_contiguous_strides_for(shape_U, row_major=False)
    U = TensorMeta(shape=shape_U, strides=strides_U, dtype=A.dtype, device=A.device)

    shape_S = batch + (k,)
    strides_S = utils.make_contiguous_strides_for(shape_S)
    S = TensorMeta(
        shape=shape_S,
        strides=strides_S,
        dtype=utils.corresponding_real_dtype(A.dtype) if A.is_complex() else A.dtype,
        device=A.device,
    )

    shape_Vh = batch + (n if full_matrices else k, n)
    # The CPU backend returns V, but the cuSolver backend returns V^H
    # TODO The MAGMA backend returns V, so this is wrong if used with the MAGMA backend
    is_cuda = A.device.type == "cuda"
    strides_Vh = utils.make_contiguous_strides_for(shape_Vh, row_major=is_cuda)
    Vh = TensorMeta(shape=shape_Vh, strides=strides_Vh, dtype=A.dtype, device=A.device)
    # Also makes sure this is CUDA or HIP:
    # https://pytorch.org/docs/stable/notes/hip.html#checking-for-hip
    if A.numel() != 0 and Vh.is_complex() and torch.cuda.is_available():
        Vh = Vh.conj()
    return U, S, Vh

