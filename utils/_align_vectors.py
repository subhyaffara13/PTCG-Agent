
def _align_vectors(a: Array, b: Array, weights: Array) -> tuple[Array, Array, Array]:
    xp = array_namespace(a)
    device = xp_device(a)
    B = (weights[:, None] * a).mT @ b
    u, s, vh = xp.linalg.svd(B)

    # Correct improper rotation if necessary (as in Kabsch algorithm)
    neg_det = xp.linalg.det(u @ vh) < 0
    s = xpx.at(s)[..., -1].set(xp.where(neg_det, -s[..., -1], s[..., -1]))
    u = xpx.at(u)[..., :, -1].set(xp.where(neg_det, -u[..., :, -1], u[..., :, -1]))

    C = u @ vh

    # DECISION: We cannot branch on the condition because jit code needs to be
    # non-branching. Hence, we omit the check for uniqueness
    # (s[1] + s[2] < 1e-16 * s[0])
    ssd = xp.sum(weights * xp.sum(b**2 + a**2, axis=-1), axis=-1) - 2 * xp.sum(
        s, axis=-1
    )
    rssd = xp.sqrt(xp.maximum(ssd, xp.zeros(1, device=device)))[..., 0]

    # TODO: We currently need to always compute the sensitivity matrix because lazy code
    # needs to be non-branching. We should check if compilers can optimize the where
    # statement (e.g. in jax) and check if we can have an eager version that only
    # evaluates the branch that is needed.
    # See xpx.apply_where, issue: https://github.com/data-apis/array-api-extra/pull/141
    zeta = (s[..., 0] + s[..., 1]) * (s[..., 1] + s[..., 2]) * (s[..., 2] + s[..., 0])
    kappa = s[..., 0] * s[..., 1] + s[..., 1] * s[..., 2] + s[..., 2] * s[..., 0]
    eye = xp.eye(3, dtype=a.dtype, device=device)
    sensitivity = xp.mean(weights) / zeta * (kappa * eye + B @ B.mT)
    q_opt = _from_matrix_orthogonal(C)
    return q_opt, rssd, sensitivity

