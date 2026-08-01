
def zero(input: TensorLikeType) -> TensorLikeType:
    return torch.zeros_like(input)


def zero(g: jit_utils.GraphContext, self):
    self_dtype = symbolic_helper._try_get_scalar_type(self)
    return zeros_like(g, self, self_dtype)


def zero(request):
    """
    Several types of scalar zeros and length 5 vectors of zeros.

    This fixture can be used to check that numeric-dtype indexes handle
    division by any zero numeric-dtype.

    Uses vector of length 5 for broadcasting with `numeric_idx` fixture,
    which creates numeric-dtype vectors also of length 5.

    Examples
    --------
    arr = RangeIndex(5)
    arr / zeros
    Index([nan, inf, inf, inf, inf], dtype='float64')
    """
    return request.param

