
def _yeojohnson_transform(x, lmbda, xp=None):
    """Returns `x` transformed by the Yeo-Johnson power transform with given
    parameter `lmbda`.
    """
    xp = array_namespace(x) if xp is None else xp
    dtype = xp_result_type(x, lmbda, force_floating=True, xp=xp)
    eps = xp.finfo(dtype).eps
    out = xp.zeros_like(x, dtype=dtype)
    pos = x >= 0  # binary mask

    if is_jax(xp):
        return xp.select(
            [(abs(lmbda) < eps) & pos, (abs(lmbda - 2) < eps) & ~pos, pos],
            [xp.log1p(x), -xp.log1p(-x), xp.expm1(lmbda * xp.log1p(x)) / lmbda],
            -xp.expm1((2 - lmbda) * xp.log1p(-x)) / (2 - lmbda),
        )

    # when x >= 0
    if abs(lmbda) < eps:
        out = xpx.at(out)[pos].set(xp.log1p(x[pos]))
    else:  # lmbda != 0
        # more stable version of: ((x + 1) ** lmbda - 1) / lmbda
        out = xpx.at(out)[pos].set(xp.expm1(lmbda * xp.log1p(x[pos])) / lmbda)

    # when x < 0
    if abs(lmbda - 2) > eps:
        out = xpx.at(out)[~pos].set(
            -xp.expm1((2 - lmbda) * xp.log1p(-x[~pos])) / (2 - lmbda))
    else:  # lmbda == 2
        out = xpx.at(out)[~pos].set(-xp.log1p(-x[~pos]))

    return out

