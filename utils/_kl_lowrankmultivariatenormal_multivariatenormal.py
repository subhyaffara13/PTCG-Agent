
def _kl_lowrankmultivariatenormal_multivariatenormal(p, q):
    if p.event_shape != q.event_shape:
        raise ValueError(
            "KL-divergence between two (Low Rank) Multivariate Normals with\
                          different event shapes cannot be computed"
        )

    term1 = 2 * q._unbroadcasted_scale_tril.diagonal(dim1=-2, dim2=-1).log().sum(
        -1
    ) - _batch_lowrank_logdet(
        p._unbroadcasted_cov_factor, p._unbroadcasted_cov_diag, p._capacitance_tril
    )
    term3 = _batch_mahalanobis(q._unbroadcasted_scale_tril, (q.loc - p.loc))
    # Expands term2 according to
    # inv(qcov) @ pcov = inv(q_tril @ q_tril.T) @ (pW @ pW.T + pD)
    combined_batch_shape = torch._C._infer_size(
        q._unbroadcasted_scale_tril.shape[:-2], p._unbroadcasted_cov_factor.shape[:-2]
    )
    n = p.event_shape[0]
    q_scale_tril = q._unbroadcasted_scale_tril.expand(combined_batch_shape + (n, n))
    p_cov_factor = p._unbroadcasted_cov_factor.expand(
        combined_batch_shape + (n, p.cov_factor.size(-1))
    )
    p_cov_diag = torch.diag_embed(p._unbroadcasted_cov_diag.sqrt()).expand(
        combined_batch_shape + (n, n)
    )
    term21 = _batch_trace_XXT(
        torch.linalg.solve_triangular(q_scale_tril, p_cov_factor, upper=False)
    )
    term22 = _batch_trace_XXT(
        torch.linalg.solve_triangular(q_scale_tril, p_cov_diag, upper=False)
    )
    term2 = term21 + term22
    return 0.5 * (term1 + term2 + term3 - p.event_shape[0])

