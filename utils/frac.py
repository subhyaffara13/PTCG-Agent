
def frac(value):
    """return fractional part of x"""
    return value - floor(value)


def frac(x: TensorLikeType) -> TensorLikeType:
    trunc_x = torch.mul(torch.floor(torch.abs(x)), torch.sign(x))
    return torch.sub(x, trunc_x)

