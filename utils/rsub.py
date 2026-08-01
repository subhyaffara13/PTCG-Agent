
def rsub(
    a: TensorLikeType | NumberType,
    b: TensorLikeType | NumberType,
    alpha: NumberType = 1,
):
    if isinstance(a, Number):
        msg = "Received a Number for the first argument, but expected a Tensor"
        raise ValueError(msg)

    return torch.sub(b, a, alpha=alpha)


def rsub(g: jit_utils.GraphContext, self, other, alpha=None):
    return sub(g, other, self, alpha=alpha)


def rsub(left, right):
    return right - left

