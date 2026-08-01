
def _kl_multivariatenormal_lowrankmultivariatenormal(p, q):
    if p.event_shape != q.event_shape:
        raise ValueError(
            "KL-divergence between two (Low Rank) Multivariate Normals with\
                          different event shapes cannot be computed"
        )

    term1 = _batch_lowrank_logdet(
        q._unbroadcasted_cov_factor, q._unbroadcasted_cov_diag, q._capacitance_tril
    ) - 2 * p._unbroadcasted_scale_tril.diagonal(dim1=-2, dim2=-1).log().sum(-1)
    term3 = _batch_lowrank_mahalanobis(
        q._unbroadcasted_cov_factor,
        q._unbroadcasted_cov_diag,
        q.loc - p.loc,
        q._capacitance_tril,
    )
    # Expands term2 according to
    # inv(qcov) @ pcov = [inv(qD) - inv(qD) @ qW @ inv(qC) @ qW.T @ inv(qD)] @ p_tril @ p_tril.T
    #                  = [inv(qD) - A.T @ A] @ p_tril @ p_tril.T
    qWt_qDinv = q._unbroadcasted_cov_factor.mT / q._unbroadcasted_cov_diag.unsqueeze(-2)
    A = torch.linalg.solve_triangular(q._capacitance_tril, qWt_qDinv, upper=False)
    term21 = _batch_trace_XXT(
        p._unbroadcasted_scale_tril * q._unbroadcasted_cov_diag.rsqrt().unsqueeze(-1)
    )
    term22 = _batch_trace_XXT(A.matmul(p._unbroadcasted_scale_tril))
    term2 = term21 - term22
    return 0.5 * (term1 + term2 + term3 - p.event_shape[0])

