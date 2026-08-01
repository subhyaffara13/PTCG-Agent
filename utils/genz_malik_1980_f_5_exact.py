
def genz_malik_1980_f_5_exact(a, b, alphas, betas, xp):
    ndim = xp_size(a)
    a = xp.reshape(a, (*([1]*(len(alphas.shape) - 1)), ndim))
    b = xp.reshape(b, (*([1]*(len(alphas.shape) - 1)), ndim))

    return (
        (1/2)**ndim
        * 1/xp.prod(alphas, axis=-1)
        * (math.pi**(ndim/2))
        * xp.prod(
            scipy.special.erf(alphas * (betas - a))
            + scipy.special.erf(alphas * (b - betas)),
            axis=-1,
        )
    )

