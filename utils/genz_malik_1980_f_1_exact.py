import math


def genz_malik_1980_f_1_exact(a, b, r, alphas, xp):
    ndim = xp_size(a)
    a = xp.reshape(a, (*([1]*(len(alphas.shape) - 1)), ndim))
    b = xp.reshape(b, (*([1]*(len(alphas.shape) - 1)), ndim))

    return (
        (-2)**ndim
        * 1/xp.prod(alphas, axis=-1)
        * xp.cos(2*math.pi*r + xp.sum(alphas * (a+b) * 0.5, axis=-1))
        * xp.prod(xp.sin(alphas * (a-b)/2), axis=-1)
    )

