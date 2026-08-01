
def _relative_error(f, A, perturbation):
    X = f(A)
    X_prime = f(A + perturbation)
    return norm(X_prime - X) / norm(X)

