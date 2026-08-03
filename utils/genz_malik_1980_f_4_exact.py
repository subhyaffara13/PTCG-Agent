import math


def genz_malik_1980_f_4_exact(a, b, alphas, xp):
    ndim = xp_size(a)

    def F(x):
        x_reshaped = xp.reshape(x, (*([1]*(len(alphas.shape) - 1)), ndim))

        return (
            (-1)**ndim/xp.prod(alphas, axis=-1)
            / math.factorial(ndim)
            / (1 + xp.sum(alphas * x_reshaped, axis=-1))
        )

    return _eval_indefinite_integral(F, a, b, xp)

