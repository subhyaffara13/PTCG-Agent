
def assoc_legendre_p_boost_(nu, mu, x):
    # the boost test data is for integer orders only
    return lpmv(mu, nu.astype(int), x)

