
def var_mean(x, axis=None, *, correction=None, keepdim=False):
    return var_mean_helper_(
        x, axis=axis, correction=correction, keepdim=keepdim, return_mean=True
    )


def var_mean(
    a: TensorLikeType,
    dim: DimsType | None = None,
    unbiased: bool | None = None,
    keepdim: bool = False,
    *,
    correction: NumberType | None = None,
):
    dim, unbiased = _dim_var_dispatch(dim, unbiased)
    v = var(a, dim, unbiased, keepdim, correction=correction)
    m = mean(a, dim, keepdim)
    return v, m


def var_mean(g: jit_utils.GraphContext, input, *args):
    if len(args) == 1:
        return _var_mean(g, input, None, args[0], None)
    else:
        return _var_mean(g, input, *args)

