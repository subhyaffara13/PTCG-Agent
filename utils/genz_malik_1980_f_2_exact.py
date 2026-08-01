
def genz_malik_1980_f_2_exact(a, b, alphas, betas, xp):
    ndim = xp_size(a)
    a = xp.reshape(a, (*([1]*(len(alphas.shape) - 1)), ndim))
    b = xp.reshape(b, (*([1]*(len(alphas.shape) - 1)), ndim))

    return (
        (-1)**ndim * 1/xp.prod(alphas, axis=-1)
        * xp.prod(
            xp.atan((a - betas)/alphas) - xp.atan((b - betas)/alphas),
            axis=-1,
        )
    )

