
def masked_fill_(
    a: TensorLikeType, mask: TensorLikeType, value: TensorOrNumberLikeType
) -> TensorLikeType:
    b = torch.masked_fill(a, mask, value)  # type: ignore[arg-type]
    a.copy_(b)
    return a


def masked_fill_(g: jit_utils.GraphContext, self, mask, value):
    return masked_fill(g, self, mask, value)

