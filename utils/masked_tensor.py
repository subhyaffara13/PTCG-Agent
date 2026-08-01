
def masked_tensor(
    data: object, mask: object, requires_grad: bool = False
) -> MaskedTensor:
    return MaskedTensor(data, mask, requires_grad)

