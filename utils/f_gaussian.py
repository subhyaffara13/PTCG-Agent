
def f_gaussian(x, alphas, xp):
    r"""
    .. math::

        f(\mathbf x) = \exp\left(-\sum^n_{i = 1} (\alpha_i x_i)^2 \right)
    """
    npoints, ndim = x.shape[0], x.shape[-1]
    alphas_reshaped = alphas[None, ...]
    x_reshaped = xp.reshape(x, (npoints, *([1]*(len(alphas.shape) - 1)), ndim))

    return xp.exp(-xp.sum((alphas_reshaped * x_reshaped)**2, axis=-1))

