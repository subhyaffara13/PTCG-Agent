
def _logm_force_nonsingular_triangular_matrix(T, inplace=False):
    # The input matrix should be upper triangular.
    # The eps is ad hoc and is not meant to be machine precision.
    tri_eps = 1e-20
    abs_diag = np.absolute(np.diag(T))
    if np.any(abs_diag == 0):
        exact_singularity_msg = 'The logm input matrix is exactly singular.'
        warnings.warn(exact_singularity_msg, LogmExactlySingularWarning, stacklevel=3)
        if not inplace:
            T = T.copy()
        n = T.shape[0]
        for i in range(n):
            if not T[i, i]:
                T[i, i] = tri_eps
    elif np.any(abs_diag < tri_eps):
        near_singularity_msg = 'The logm input matrix may be nearly singular.'
        warnings.warn(near_singularity_msg, LogmNearlySingularWarning, stacklevel=3)
    return T

