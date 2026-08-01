
def check_jac_sparsity(jac_sparsity, m, n):
    if jac_sparsity is None:
        return None

    if not issparse(jac_sparsity):
        jac_sparsity = np.atleast_2d(jac_sparsity)

    if jac_sparsity.shape != (m, n):
        raise ValueError("`jac_sparsity` has wrong shape.")

    return jac_sparsity, group_columns(jac_sparsity)

