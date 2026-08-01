
def genz_malik_1980_f_2(x, alphas, betas, xp):
    r"""
    .. math:: f_2(\mathbf x) = \prod^n_{i = 1} (\alpha_i^2 + (x_i - \beta_i)^2)^{-1}

    .. code-block:: mathematica

        genzMalik1980f2[x_List, alphas_List, betas_List] :=
            1/Times @@ ((alphas^2 + (x - betas)^2))
    """
    npoints, ndim = x.shape[0], x.shape[-1]

    alphas_reshaped = alphas[None, ...]
    betas_reshaped = betas[None, ...]

    x_reshaped = xp.reshape(x, (npoints, *([1]*(len(alphas.shape) - 1)), ndim))

    return 1/xp.prod(alphas_reshaped**2 + (x_reshaped-betas_reshaped)**2, axis=-1)

