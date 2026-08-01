
def qr_normal_byrd_omojokun(aub, free_xl, free_xu, free_slack, free_ub):
    m_linear_ub, n = aub.shape
    identity_n = np.eye(n)
    identity_m = np.eye(m_linear_ub)
    q, r, _ = qr(
        np.block(
            [
                [
                    aub[~free_ub, :],
                    -identity_m[~free_ub, :],
                ],
                [
                    np.zeros((m_linear_ub - np.count_nonzero(free_slack), n)),
                    -identity_m[~free_slack, :],
                ],
                [
                    -identity_n[~free_xl, :],
                    np.zeros((n - np.count_nonzero(free_xl), m_linear_ub)),
                ],
                [
                    identity_n[~free_xu, :],
                    np.zeros((n - np.count_nonzero(free_xu), m_linear_ub)),
                ],
            ]
        ).T,
        pivoting=True,
    )
    n_act = np.count_nonzero(
        np.abs(np.diag(r))
        >= 10.0
        * EPS
        * (n + m_linear_ub)
        * np.linalg.norm(r[: np.min(r.shape), : np.min(r.shape)], axis=0)
    )
    return n_act, q

