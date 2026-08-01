
def genz_malik_1980_f_3(x, alphas, xp):
    r"""
    .. math:: f_3(\mathbf x) = \exp\left(\sum^n_{i = 1} \alpha_i x_i\right)

    .. code-block:: mathematica

        genzMalik1980f3[x_List, alphas_List] := Exp[Dot[x, alphas]]
    """

    npoints, ndim = x.shape[0], x.shape[-1]

    alphas_reshaped = alphas[None, ...]
    x_reshaped = xp.reshape(x, (npoints, *([1]*(len(alphas.shape) - 1)), ndim))

    return xp.exp(xp.sum(alphas_reshaped * x_reshaped, axis=-1))

