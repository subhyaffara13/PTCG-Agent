
def _help_expm_cond_search(A, A_norm, X, X_norm, eps, p):
    p = np.reshape(p, A.shape)
    p_norm = norm(p)
    perturbation = eps * p * (A_norm / p_norm)
    X_prime = expm(A + perturbation)
    scaled_relative_error = norm(X_prime - X) / (X_norm * eps)
    return -scaled_relative_error

