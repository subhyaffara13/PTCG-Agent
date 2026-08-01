
def _align_vectors_fixed(
    a: Array, b: Array, weights: Array
) -> tuple[Array, Array, Array]:
    xp = array_namespace(a)
    device = xp_device(a)
    N = a.shape[0]
    weight_is_inf = xp.asarray([True], device=device) if N == 1 else weights == xp.inf
    # We cannot use boolean masks for indexing because of jax. For the same reason, we
    # also cannot use dynamic slices. As a workaround, we roll the array so that the
    # infinitely weighted vector is at index 0. We then use static slices to get the
    # primary and secondary vectors.
    #
    # Note that argmax fulfils a secondary purpose here:
    # When we trace this function with jax, this function might get executed even if
    # weight_is_inf does not have a single valid entry. Argmax will still give us a
    # valid index which allows us to proceed with the function (the results are
    # discarded anyways), whereas boolean indexing would result in invalid, zero-shaped
    # arrays.

    inf_idx = xp.argmax(xp.astype(weight_is_inf, xp.uint8))
    # xp.argmax returns an Array, but the specification of xp.roll does not support
    # Arrays as shifts. For lazy execution models we cannot convert to int because this
    # raises a concretization error. However, jax does accept Arrays as shifts which
    # allows jit compiling the function. Hence we do not convert to int for jax.
    # See https://github.com/data-apis/array-api/issues/914#issuecomment-2918959918
    if not is_jax(xp):
        inf_idx = int(inf_idx)
    a_sorted = xp.roll(a, shift=-inf_idx, axis=0)
    b_sorted = xp.roll(b, shift=-inf_idx, axis=0)
    weights_sorted = xp.roll(weights, shift=-inf_idx, axis=0)

    a_pri = a_sorted[0, ...][None, ...]  # Effectively [[0], ...]
    b_pri = b_sorted[0, ...][None, ...]
    a_pri_norm = xp_vector_norm(a_pri, axis=-1, keepdims=True, xp=xp)
    b_pri_norm = xp_vector_norm(b_pri, axis=-1, keepdims=True, xp=xp)
    if not is_lazy_array(a_pri_norm):
        if xp.any(a_pri_norm == 0) or xp.any(b_pri_norm == 0):
            raise ValueError("Cannot align zero length primary vectors")

    # We cannot error out on zero length vectors. We set the norm to NaN to avoid
    # division by zero and mark the result as invalid.
    a_pri_norm = xpx.at(a_pri_norm)[a_pri_norm == 0].set(xp.nan)
    b_pri_norm = xpx.at(b_pri_norm)[b_pri_norm == 0].set(xp.nan)

    a_pri = a_pri / a_pri_norm
    b_pri = b_pri / b_pri_norm

    # We first find the minimum angle rotation between the primary
    # vectors.
    cross = xp.linalg.cross(b_pri[..., 0, :], a_pri[..., 0, :])
    cross_norm = xp_vector_norm(cross, axis=-1, xp=xp)
    theta = xp.atan2(cross_norm, xp.sum(a_pri[..., 0, :] * b_pri[..., 0, :], axis=-1))
    tolerance = 1e-3  # tolerance for small angle approximation (rad)
    q_flip = xp.asarray([0.0, 0.0, 0.0, 1.0], dtype=a_pri.dtype, device=device)

    # Near pi radians, the Taylor series approximation of x/sin(x) diverges, so for
    # numerical stability we flip pi and then rotate back by the small angle pi - theta
    flip = xp.pi - theta < tolerance
    # For antiparallel vectors, cross = [0, 0, 0] so we need to manually set an
    # arbitrary orthogonal axis of rotation
    i = xp.argmin(xp.abs(a_pri[..., 0, :]))
    # TODO: Array API does not support fancy indexing __setitem__. The code is
    # equivalent to doing the following:
    # r_components = xp.zeros(3)
    # r_components = xpx.at(r_components)[i - 1].set(a_pri[0, i - 2])
    # r_components = xpx.at(r_components)[i - 2].set(-a_pri[0, i - 1])
    r_components = xp.stack(
        [
            xp.where(i == 1, a_pri[0, 2], xp.where(i == 2, -a_pri[0, 1], 0)),
            xp.where(i == 2, a_pri[0, 0], xp.where(i == 0, -a_pri[0, 2], 0)),
            xp.where(i == 0, a_pri[0, 1], xp.where(i == 1, -a_pri[0, 0], 0)),
        ]
    )
    r = xp.where(cross_norm == 0, r_components, cross)

    q_flip = xp.where(flip, from_rotvec(r / xp_vector_norm(r, xp=xp) * xp.pi), q_flip)
    theta = xp.where(flip, xp.pi - theta, theta)
    cross = xp.where(flip, -cross, cross)

    # Small angle Taylor series approximation for numerical stability
    theta2 = theta * theta
    small_scale = xp.abs(theta) < tolerance
    r_small_scale = cross * (1 + theta2 / 6 + theta2 * theta2 * 7 / 360)
    # We need to handle the case where theta is 0 to avoid division by zero. We use the
    # value of the Taylor series approximation, but non-branching operations require
    # that we still divide by the angle. Since we do not use the result where the angle
    # is close to 0, this is safe.
    theta = theta + xp.asarray(small_scale, dtype=theta.dtype)
    r_large_scale = cross * theta / xp.sin(theta)
    r = xp.where(small_scale, r_small_scale, r_large_scale)
    q_pri = compose_quat(from_rotvec(r), q_flip)

    # Case 1): No secondary vectors, q_opt is q_pri -> Immediately done
    # Case 2): Secondary vectors exist
    # We cannot use boolean masks here because of jax
    a_sec = a_sorted[1:, ...]
    b_sec = b_sorted[1:, ...]
    weights_sec = weights_sorted[1:]

    # We apply the first rotation to the b vectors to align the
    # primary vectors, resulting in vectors c. The secondary
    # vectors must now be rotated about that primary vector to best
    # align c to a.
    c_sec = apply(q_pri, b_sec)

    # Calculate vector components for the angle calculation. The
    # angle phi to rotate a single 2D vector C to align to 2D
    # vector A in the xy plane can be found with the equation
    # phi = atan2(cross(C, A), dot(C, A))
    #     = atan2(|C|*|A|*sin(phi), |C|*|A|*cos(phi))
    # The below equations perform the same operation, but with the
    # 3D rotation restricted to the 2D plane normal to a_pri, where
    # the secondary vectors are projected into that plane. We then
    # find the composite angle from the weighted sum of the
    # axial components in that plane, minimizing the 2D alignment
    # problem.
    sin_term = xp.linalg.vecdot(xp.linalg.cross(c_sec, a_sec), a_pri)
    cos_term = xp.linalg.vecdot(c_sec, a_sec) - (
        xp.linalg.vecdot(c_sec, a_pri) * xp.linalg.vecdot(a_sec, a_pri)
    )
    phi = xp.atan2(xp.sum(weights_sec * sin_term), xp.sum(weights_sec * cos_term))
    q_sec = from_rotvec(phi * a_pri[0, ...])

    # Compose these to get the optimal rotation
    q_opt = q_pri if N == 1 else compose_quat(q_sec, q_pri)

    # Calculate the root sum squared distance. We force the error to
    # be zero for the infinite weight vectors since they will align
    # exactly.
    mask = ((N > 1) | (weights[0] == xp.inf)) & weight_is_inf
    # Skip non-infinite weight single vectors pairs, we used the
    # infinite weight code path but don't want to zero that weight
    weights_inf_zero = xpx.at(weights, mask).set(0, copy=True, xp=xp)
    a_est = apply(q_opt, b)
    rssd = xp.sqrt(xp.sum(weights_inf_zero @ (a - a_est) ** 2))

    mask = xp.any(xp.isnan(weights), axis=-1)
    q_opt = xp.where(mask, xp.nan, q_opt)
    return q_opt, rssd, xp.asarray(xp.nan, device=device)

