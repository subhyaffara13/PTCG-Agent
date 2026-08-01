
def async_wrong_type():
    return torch.zeros(2, 2)


def async_wrong_type() -> Tensor:
    return torch.zeros(2)

