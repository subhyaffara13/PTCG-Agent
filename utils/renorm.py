
def renorm(
    input: TensorLikeType, p: RealNumberType, dim: int, maxnorm: RealNumberType
) -> TensorLikeType:
    torch._check(not isinstance(p, complex), lambda: "renorm: p must be real-valued")
    torch._check(p > 0, lambda: "renorm: non-positive norm not supported")
    torch._check(
        not isinstance(maxnorm, complex), lambda: "renorm: maxnorm must be real-valued"
    )
    torch._check(
        maxnorm >= 0, lambda: f"renorm: expected maxnorm to be >= 0 but got {maxnorm}"
    )
    ndim = input.ndim
    torch._check(
        ndim > 1,
        lambda: f"renorm: input needs at least 2 dimensions, got {ndim} dimensions",
    )

    dim = utils.canonicalize_dim(ndim, dim)
    reduce_dims = list(range(ndim))
    del reduce_dims[dim]

    # For half and bfloat16, calculate norm in float precision then cast
    # normalization factor to half
    acc_type = utils.get_computation_dtype(input.dtype)
    if acc_type != input.dtype:
        norm = torch.linalg.vector_norm(
            input, p, reduce_dims, keepdim=True, dtype=acc_type
        )
    else:
        norm = torch.linalg.vector_norm(input, p, reduce_dims, keepdim=True)

    eps = 1e-7
    norm_factor = torch.where(norm > maxnorm, maxnorm / (norm + eps), 1.0)
    if acc_type != input.dtype:
        norm_factor = prims.convert_element_type(norm_factor, input.dtype)
    return (input * norm_factor).contiguous()

