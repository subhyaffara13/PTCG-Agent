
def _kl_multivariatenormal_multivariatenormal(p, q):
    # From https://en.wikipedia.org/wiki/Multivariate_normal_distribution#Kullback%E2%80%93Leibler_divergence
    if p.event_shape != q.event_shape:
        raise ValueError(
            "KL-divergence between two Multivariate Normals with\
                          different event shapes cannot be computed"
        )

    half_term1 = q._unbroadcasted_scale_tril.diagonal(dim1=-2, dim2=-1).log().sum(
        -1
    ) - p._unbroadcasted_scale_tril.diagonal(dim1=-2, dim2=-1).log().sum(-1)
    combined_batch_shape = torch._C._infer_size(
        q._unbroadcasted_scale_tril.shape[:-2], p._unbroadcasted_scale_tril.shape[:-2]
    )
    n = p.event_shape[0]
    q_scale_tril = q._unbroadcasted_scale_tril.expand(combined_batch_shape + (n, n))
    p_scale_tril = p._unbroadcasted_scale_tril.expand(combined_batch_shape + (n, n))
    term2 = _batch_trace_XXT(
        torch.linalg.solve_triangular(q_scale_tril, p_scale_tril, upper=False)
    )
    term3 = _batch_mahalanobis(q._unbroadcasted_scale_tril, (q.loc - p.loc))
    return half_term1 + 0.5 * (term2 + term3 - n)

