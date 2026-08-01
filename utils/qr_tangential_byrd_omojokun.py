
def qr_tangential_byrd_omojokun(aub, aeq, free_xl, free_xu, free_ub):
    n = free_xl.size
    identity = np.eye(n)
    q, r, _ = qr(
        np.block(
            [
                [aeq],
                [aub[~free_ub, :]],
                [-identity[~free_xl, :]],
                [identity[~free_xu, :]],
            ]
        ).T,
        pivoting=True,
    )
    n_act = np.count_nonzero(
        np.abs(np.diag(r))
        >= 10.0
        * EPS
        * n
        * np.linalg.norm(r[: np.min(r.shape), : np.min(r.shape)], axis=0)
    )
    return n_act, q

