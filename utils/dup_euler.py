
def dup_euler(n, K):
    """Low-level implementation of Euler polynomials."""
    return dup_quo_ground(dup_genocchi(n+1, ZZ), K(-n-1), K)

