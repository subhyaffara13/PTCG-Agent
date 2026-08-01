
def as_masked_tensor(data: object, mask: object) -> MaskedTensor:
    return MaskedTensor._from_values(data, mask)

