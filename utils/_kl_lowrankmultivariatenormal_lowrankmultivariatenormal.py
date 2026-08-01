
def _kl_lowrankmultivariatenormal_lowrankmultivariatenormal(p, q):
    if p.event_shape != q.event_shape:
        raise ValueError(
            "KL-divergence between two Low Rank Multivariate Normals with\
                          different event shapes cannot be computed"
        )

    term1 = _batch_lowrank_logdet(
        q._unbroadcasted_cov_factor, q._unbroadcasted_cov_diag, q._capacitance_tril
    ) - _batch_lowrank_logdet(
        p._unbroadcasted_cov_factor, p._unbroadcasted_cov_diag, p._capacitance_tril
    )
    term3 = _batch_lowrank_mahalanobis(
        q._unbroadcasted_cov_factor,
        q._unbroadcasted_cov_diag,
        q.loc - p.loc,
        q._capacitance_tril,
    )
    # Expands term2 according to
    # inv(qcov) @ pcov = [inv(qD) - inv(qD) @ qW @ inv(qC) @ qW.T @ inv(qD)] @ (pW @ pW.T + pD)
    #                  = [inv(qD) - A.T @ A] @ (pD + pW @ pW.T)
    qWt_qDinv = q._unbroadcasted_cov_factor.mT / q._unbroadcasted_cov_diag.unsqueeze(-2)
    A = torch.linalg.solve_triangular(q._capacitance_tril, qWt_qDinv, upper=False)
    term21 = (p._unbroadcasted_cov_diag / q._unbroadcasted_cov_diag).sum(-1)
    term22 = _batch_trace_XXT(
        p._unbroadcasted_cov_factor * q._unbroadcasted_cov_diag.rsqrt().unsqueeze(-1)
    )
    term23 = _batch_trace_XXT(A * p._unbroadcasted_cov_diag.sqrt().unsqueeze(-2))
    term24 = _batch_trace_XXT(A.matmul(p._unbroadcasted_cov_factor))
    term2 = term21 + term22 - term23 - term24
    return 0.5 * (term1 + term2 + term3 - p.event_shape[0])

