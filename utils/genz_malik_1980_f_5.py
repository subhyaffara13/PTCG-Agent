
def genz_malik_1980_f_5(x, alphas, betas, xp):
    r"""
    .. math::

        f_5(\mathbf x) = \exp\left(-\sum^n_{i = 1} \alpha^2_i (x_i - \beta_i)^2\right)

    .. code-block:: mathematica

        genzMalik1980f5[x_List, alphas_List, betas_List] :=
            Exp[-Total[alphas^2 * (x - betas)^2]]
    """

    npoints, ndim = x.shape[0], x.shape[-1]

    alphas_reshaped = alphas[None, ...]
    betas_reshaped = betas[None, ...]

    x_reshaped = xp.reshape(x, (npoints, *([1]*(len(alphas.shape) - 1)), ndim))

    return xp.exp(
        -xp.sum(alphas_reshaped**2 * (x_reshaped - betas_reshaped)**2, axis=-1)
    )

