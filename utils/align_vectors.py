
def align_vectors(
    a: Array, b: Array, weights: Array | None = None, return_sensitivity: bool = False
) -> tuple[Array, Array, Array]:
    xp = array_namespace(a)
    # Check input vectors
    dtype = xp_result_type(a, b, force_floating=True, xp=xp)
    a_original = xp.asarray(a, dtype=dtype)
    b_original = xp.asarray(b, dtype=dtype)
    a = xpx.atleast_nd(a_original, ndim=2, xp=xp)
    b = xpx.atleast_nd(b_original, ndim=2, xp=xp)
    if a.shape[-1] != 3:
        raise ValueError(
            f"Expected input `a` to have shape (3,) or (N, 3), got {a_original.shape}"
        )
    if b.shape[-1] != 3:
        raise ValueError(
            f"Expected input `b` to have shape (3,) or (N, 3), got {b_original.shape}"
        )
    if a.shape != b.shape:
        raise ValueError(
            "Expected inputs `a` and `b` to have same shapes"
            f", got {a_original.shape} and {b_original.shape} respectively."
        )
    if a.ndim > 2 or b.ndim > 2:  # This function does not support broadcasting
        raise ValueError(
            "Expected inputs `a` and `b` to have shape (3,) or (N, 3), got "
            f"{a_original.shape} and {b_original.shape} respectively."
        )
    N = a.shape[0]

    # Check weights
    if weights is None:
        weights = xp.ones(N, device=xp_device(a), dtype=a.dtype)
    else:
        weights = xp.asarray(weights, device=xp_device(a), dtype=a.dtype)
        if weights.ndim != 1:
            raise ValueError(
                f"Expected `weights` to be 1 dimensional, got shape {weights.shape}."
            )
        if N > 1 and (weights.shape[0] != N):
            raise ValueError(
                "Expected `weights` to have number of values equal to number of input "
                f"vectors, got {weights.shape[0]} values and {N} vectors."
            )
        # We can only check for negative weights in eager execution models. Lazy
        # backends will return NaNs instead.
        negative_weights = weights < 0
        if not is_lazy_array(negative_weights) and xp.any(negative_weights):
            raise ValueError("`weights` may not contain negative values")
        weights = xp.where(negative_weights, xp.nan, weights)

    # For the special case of a single vector pair, we use the infinite
    # weight code path
    weight_is_inf = xp.asarray([True]) if N == 1 else weights == xp.inf
    n_inf = xp.sum(xp.astype(weight_is_inf, a.dtype))
    # We can only error out on multiple infinite weights or sensitivity return with
    # infinite weights in eager execution models. Lazy backends will return NaNs.
    if not is_lazy_array(n_inf):
        if n_inf > 1:
            raise ValueError("Only one infinite weight is allowed")
        if n_inf == 1 and return_sensitivity:
            raise ValueError(
                "Cannot return sensitivity matrix with an "
                "infinite weight or one vector pair"
            )

    weights = xp.where(n_inf > 1, xp.nan, weights)

    inf_branch = xp.any(weight_is_inf, axis=-1)
    # DECISION: We cannot compute both branches for all frameworks. There are two main
    # reasons:
    # 1. Computing both for eager execution models is expensive.
    # 2. Some operations will fail when running the unused branch because of numerical
    # and algorithmical issues. Numpy e.g. will raise an exception when trying to
    # compute the svd of a matrix with infinite weights. To prevent this, we only
    # compute the branch that is needed. Lazy backends however require us to take the
    # full compute graph. Therefore, we use xp.where for lazy backends and a branching
    # version for eager frameworks.
    #
    # Note that we could also solve this by exploiting the externals of xpx.apply_where.
    # However, we'd have to rely on the implementation details of apply_where, which is
    # something we should avoid.
    # See https://github.com/scipy/scipy/pull/22777#discussion_r2028868364
    if is_lazy_array(inf_branch):
        q_opt, rssd, sensitivity = _align_vectors(a, b, weights)
        q_opt_inf, rssd_inf, sensitivity_inf = _align_vectors_fixed(a, b, weights)
        q_opt = xp.where(inf_branch, q_opt_inf, q_opt)
        rssd = xp.where(inf_branch, rssd_inf, rssd)
        sensitivity = xp.where(inf_branch, sensitivity_inf, sensitivity)
    else:
        if xp.any(inf_branch):
            q_opt, rssd, sensitivity = _align_vectors_fixed(a, b, weights)
        else:
            q_opt, rssd, sensitivity = _align_vectors(a, b, weights)
    return q_opt, rssd, sensitivity

