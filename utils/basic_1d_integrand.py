
def basic_1d_integrand(x, n, xp):
    x_reshaped = xp.reshape(x, (-1, 1, 1))
    n_reshaped = xp.reshape(n, (1, -1, 1))

    return x_reshaped**n_reshaped

